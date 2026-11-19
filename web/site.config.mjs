export const repository =
  process.env.GITHUB_REPOSITORY || "cristianandfriends/say-it-then-ship-it";

if (!/^[\w.-]+\/[\w.-]+$/.test(repository)) {
  throw new Error("GITHUB_REPOSITORY must use the format owner/repository.");
}

const [owner, name] = repository.split("/");

export const site = `https://${owner}.github.io`;
export const base =
  name.toLowerCase() === `${owner}.github.io`.toLowerCase() ? "/" : `/${name}/`;
export const repositoryUrl = `https://github.com/${repository}`;
export const discordUrl = "https://discord.gg/sMafw3ktj";
export const slidesUrl =
  "https://docs.google.com/presentation/d/e/2PACX-1vRgWXcd3VTgfIUE0qp6972ijj1sA6HPSrSgOzt0O8eHMBFqTroFWwSJ43UzPcBTRos33YO6-PLOwQf6/pubembed?start=false&loop=false&delayms=3000";
export const openSlidesUrl = slidesUrl.replace("/pubembed?", "/pub?");

export function withBase(path = "") {
  return `${base}${path.replace(/^\/+/, "")}`;
}
