import { expect, test } from "@playwright/test";
import { repositoryUrl, withBase } from "../web/site.config.mjs";

test.beforeEach(async ({ page }) => {
  await page.route("https://docs.google.com/**", (route) =>
    route.fulfill({ contentType: "text/html", body: "<p>Live slide deck</p>" }),
  );
});

test("puts the deck first and links to the live chat and repository", async ({ page }) => {
  await page.goto("./");
  await expect(page.locator("main > section").first()).toHaveAttribute("id", "slides");
  await expect(page.getByTitle("Say it, then ship it: live presentation")).toHaveAttribute(
    "src",
    /\/pubembed\?start=false&loop=false&delayms=3000$/,
  );
  await expect(page.getByRole("link", { name: "Join Discord" })).toHaveAttribute(
    "href",
    "https://discord.gg/sMafw3ktj",
  );
  await expect(page.getByRole("link", { name: "Source on GitHub" })).toHaveAttribute(
    "href",
    repositoryUrl,
  );
  await page.keyboard.press("Tab");
  await expect(page.getByRole("link", { name: "Skip to content" })).toBeFocused();
});

test("renders shared Markdown, highlighted code, and Mermaid under the project base path", async ({ page, baseURL }) => {
  await page.goto("./");
  await page.getByRole("link", { name: /Work with two agents/ }).click();
  await expect(page).toHaveURL(new URL(withBase("files/lab/two-agents/"), baseURL).href);
  await expect(page.getByRole("heading", { name: "Work with two agents", exact: true })).toBeVisible();
  await expect(page.locator(".astro-code")).toHaveCount(2);
  await expect(page.locator(".diagram svg")).toBeVisible();
  await expect(page.locator(".diagram svg")).toHaveAccessibleName("The two-agent workflow");
  await expect(page.getByRole("link", { name: "View source" })).toHaveAttribute(
    "href",
    `${repositoryUrl}/blob/HEAD/lab/two-agents.md`,
  );
  await page.getByRole("link", { name: "[ Back to lab files ]", exact: true }).click();
  await expect(page).toHaveURL(new URL(withBase("#files"), baseURL).href);
});

test("keeps the home and reader pages inside a narrow mobile viewport", async ({ page }) => {
  await page.setViewportSize({ width: 320, height: 740 });
  for (const path of ["./", "files/lab/two-agents/"]) {
    await page.goto(path);
    await expect(page.getByRole("link", { name: "Join Discord" })).toBeVisible();
    expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBeLessThanOrEqual(320);
  }
});

test("keeps diagram source readable without JavaScript", async ({ browser, baseURL }) => {
  const context = await browser.newContext({ javaScriptEnabled: false });
  const page = await context.newPage();
  await page.goto(new URL("files/lab/two-agents/", baseURL).href);
  await expect(page.locator("pre[data-mermaid]")).toContainText("flowchart LR");
  await expect(page.getByRole("heading", { name: "Work with two agents", exact: true })).toBeVisible();
  await context.close();
});
