import { visit } from "unist-util-visit";

export default function remarkMermaid() {
  return (tree) => {
    visit(tree, "code", (node) => {
      if (node.lang !== "mermaid") return;

      const source = node.value
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;");

      node.type = "html";
      node.value = `<figure class="diagram"><pre data-mermaid><code>${source}</code></pre></figure>`;
    });
  };
}
