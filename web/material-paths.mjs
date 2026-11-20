export const materialRoots = [
  "lab",
  ".github/agents",
  ".github/instructions",
  ".github/skills",
  ".agents/skills",
  ".opencode",
];

export const materialFiles = ["AGENTS.md", ".github/copilot-instructions.md"];

export const materialPatterns = [
  ...materialRoots.map((root) => `${root}/**/*.md`),
  ...materialFiles,
];

export function isMaterialPath(path) {
  return (
    path.endsWith(".md") &&
    (materialFiles.includes(path) ||
      materialRoots.some((root) => path.startsWith(`${root}/`)))
  );
}

export function materialRoute(path) {
  return path.replace(/\.md$/, "").replace(/(^|\/)\./g, "$1");
}
