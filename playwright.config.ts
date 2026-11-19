import { defineConfig, devices } from "@playwright/test";
import { base } from "./web/site.config.mjs";

const baseURL = `http://127.0.0.1:47831${base}`;

export default defineConfig({
  testDir: "./tests",
  fullyParallel: true,
  use: {
    baseURL,
    ...devices["Desktop Chrome"],
  },
  webServer: {
    command: "npm run preview -- --host 127.0.0.1 --port 47831",
    url: baseURL,
    reuseExistingServer: false,
  },
});
