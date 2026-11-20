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
    "https://discord.gg/WqcQTVW6fM",
  );
  await expect(page.getByRole("link", { name: "the live Discord chat", exact: true })).toHaveAttribute(
    "href",
    "https://discord.gg/WqcQTVW6fM",
  );
  await expect(page.getByRole("link", { name: "Source on GitHub" })).toHaveAttribute(
    "href",
    repositoryUrl,
  );
  await expect(page.getByRole("banner").getByRole("link", { name: "GitHub", exact: true })).toHaveAttribute(
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
  await expect(page.locator(".astro-code").first()).toBeVisible();
  await expect(page.locator(".diagram svg")).toBeVisible();
  await expect(page.locator(".diagram svg")).toHaveAccessibleName(/\S/);
  await expect(page.getByRole("link", { name: "View source" })).toHaveAttribute(
    "href",
    `${repositoryUrl}/blob/HEAD/lab/two-agents.md`,
  );
  await page.getByRole("link", { name: "[ Back to lab files ]", exact: true }).click();
  await expect(page).toHaveURL(new URL(withBase("#files"), baseURL).href);
});

test("links to Start here and Guides from the top right of a reader", async ({ page, baseURL }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto("files/lab/two-agents/");
  const startLink = page.getByRole("banner").getByRole("link", { name: "Start here", exact: true });
  await expect(startLink).toHaveAttribute("href", withBase("files/lab/start-here/"));
  const guidesLink = page.getByRole("banner").getByRole("link", { name: "Guides", exact: true });
  await expect(guidesLink).toHaveAttribute("href", withBase("#guides"));
  const headerBounds = await page.getByRole("banner").boundingBox();
  for (const link of [startLink, guidesLink]) {
    const linkBounds = await link.boundingBox();
    expect(linkBounds!.x).toBeGreaterThan(headerBounds!.x + headerBounds!.width / 2);
  }

  await startLink.click();
  await expect(page).toHaveURL(new URL(withBase("files/lab/start-here/"), baseURL).href);
  await expect(page.getByRole("heading", { name: "Start here", exact: true })).toBeVisible();
  await guidesLink.click();
  await expect(page).toHaveURL(new URL(withBase("#guides"), baseURL).href);
  const guides = page.getByRole("region", { name: "Guides", exact: true });
  await expect(guides).toBeInViewport();
  await expect(guides.getByRole("link", { name: /Work with two agents/ })).toBeVisible();
});

test("renders supplementary guides with accessible diagrams on mobile", async ({ page }) => {
  await page.goto("./#guides");
  const guides = page.getByRole("region", { name: "Guides", exact: true });
  const paths = await guides.locator('a[href*="/files/lab/"]').evaluateAll((links) =>
    links.map((link) => link.getAttribute("href")!)
      .filter((href) => !href.endsWith("/start-here/")),
  );
  expect(paths.length).toBeGreaterThanOrEqual(4);

  await page.setViewportSize({ width: 320, height: 740 });
  for (const path of paths) {
    await page.goto(path);
    await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
    await expect(page.locator(".diagram svg").first()).toBeVisible();
    await expect(page.locator(".diagram svg").first()).toHaveAccessibleName(/\S/);
    await expect(page.locator(".diagram-message")).toHaveCount(0);
    expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBeLessThanOrEqual(320);
  }
});

test("keeps the home and reader pages inside a narrow mobile viewport", async ({ page }) => {
  await page.setViewportSize({ width: 320, height: 740 });
  for (const path of [
    "./",
    "files/lab/two-agents/",
    "files/lab/level-0-bootstrap/",
    "files/lab/level-4-agent/",
    "files/agents/skills/bootstrap-lab/SKILL/",
    "files/opencode/agents/software-engineering-expert/",
  ]) {
    await page.goto(path);
    await expect(page.getByRole("link", { name: "Join Discord" })).toBeVisible();
    await expect(page.getByRole("banner").getByRole("link", { name: "GitHub", exact: true })).toBeVisible();
    await expect(page.getByRole("banner").getByRole("link", { name: "Guides", exact: true })).toBeVisible();
    await expect(page.getByRole("banner").getByRole("link", { name: "Start here", exact: true })).toBeVisible();
    const brandBounds = await page.locator(".brand").boundingBox();
    const linksBounds = await page.locator(".header-links").boundingBox();
    expect(brandBounds!.x + brandBounds!.width).toBeLessThanOrEqual(linksBounds!.x);
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

test("lists the lab sequence before reusable tools and keeps references out of the directory", async ({ page }) => {
  await page.goto("./");
  const levels = page.getByRole("region", { name: "Lab levels", exact: true });
  const titles = await levels.locator(".file-title").allTextContents();
  expect(titles).toHaveLength(8);
  titles.forEach((title, level) => expect(title).toMatch(new RegExp(`^Level ${level}:`)));

  const tools = page.getByRole("region", { name: "Agents and skills", exact: true });
  await expect(tools.locator(".file-link")).toHaveCount(5);
  await expect(page.locator(".file-path").filter({ hasText: "/references/" })).toHaveCount(0);

  await levels.getByRole("link").first().click();
  await page.locator(`.prose a[href="${withBase("files/lab/level-1-brief/")}"]`).last().click();
  await expect(page.getByRole("heading", { level: 1 })).toHaveText(/^Level 1:/);
});

test("connects skill creation to the project specialist and review levels", async ({ page }) => {
  await page.goto("files/lab/level-3-skill/");
  await page.locator(".prose").getByRole("link", {
    name: "Level 4: Make a specialized subagent", exact: true,
  }).click();
  await expect(page.getByRole("heading", { level: 1 })).toHaveText(
    "Level 4: Make a specialized subagent",
  );
  await expect(page.locator(".diagram svg")).toBeVisible();
  await expect(page.locator(".diagram svg")).toHaveAccessibleName(/\S/);
  await page.locator(".prose").getByRole("link", {
    name: "Level 5: Extend and review", exact: true,
  }).click();
  await expect(page.getByRole("heading", { level: 1 })).toHaveText(
    "Level 5: Extend and review",
  );
});

test("preserves published reader links after renumbering the later levels", async ({ page, baseURL }) => {
  for (const [previous, current, title] of [
    ["level-4-review", "level-5-review", "Level 5: Extend and review"],
    ["level-5-context", "level-6-context", "Level 6: Hand off the context"],
    ["level-6-tools", "level-7-tools", "Level 7: Try a read-only MCP tool"],
  ]) {
    await page.goto(`files/lab/${previous}/`);
    await expect(page).toHaveURL(new URL(withBase(`files/lab/${current}/`), baseURL).href);
    await expect(page.getByRole("heading", { level: 1 })).toHaveText(title);
  }
});

test("publishes the native OpenCode agent in the material directory", async ({ page }) => {
  await page.goto("./");
  await page.getByRole("region", { name: "Agents and skills", exact: true })
    .locator(`a[href="${withBase("files/opencode/agents/software-engineering-expert/")}"]`).click();
  await expect(page.getByRole("heading", { name: "Software engineering expert", exact: true })).toBeVisible();
  await expect(page.getByRole("link", { name: "View source" })).toHaveAttribute(
    "href",
    `${repositoryUrl}/blob/HEAD/.opencode/agents/software-engineering-expert.md`,
  );
});

test("resolves bundled skill references into readable site pages", async ({ page, baseURL }) => {
  await page.goto("files/agents/skills/stop-slop/SKILL/");
  const reference = page.locator(".prose a").filter({ hasText: "references/phrases.md" }).first();
  await expect(reference).toHaveAttribute(
    "href",
    withBase("files/agents/skills/stop-slop/references/phrases/"),
  );
  await reference.click();
  await expect(page).toHaveURL(new URL(withBase("files/agents/skills/stop-slop/references/phrases/"), baseURL).href);
  await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
});
