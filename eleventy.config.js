// Eleventy configuration for the EyeTRU website.
// Content lives in src/content/ (one file per item) and src/_data/ (site settings).
// Editors normally change content through Pages CMS (see .pages.yml), never this file.
import yaml from "js-yaml";
import { HtmlBasePlugin } from "@11ty/eleventy";

const STATUS_ORDER = ["published", "accepted", "in-review", "submitted", "ready", "in-preparation"];

export default function (eleventyConfig) {
  eleventyConfig.addPlugin(HtmlBasePlugin);
  eleventyConfig.addDataExtension("yml,yaml", (contents) => yaml.load(contents));

  eleventyConfig.addPassthroughCopy({ "src/assets": "assets" });
  eleventyConfig.addPassthroughCopy({ "src/static": "/" });

  // ---------- Collections (one folder per type in src/content) ----------
  const glob = (name) => `src/content/${name}/*.md`;
  const sortByOrderThenName = (a, b) =>
    (a.data.order ?? 999) - (b.data.order ?? 999) || String(a.data.name ?? a.data.title).localeCompare(String(b.data.name ?? b.data.title));

  eleventyConfig.addCollection("people", (api) =>
    api.getFilteredByGlob(glob("people")).filter((p) => !p.data.hidden).sort(sortByOrderThenName));

  eleventyConfig.addCollection("projects", (api) =>
    api.getFilteredByGlob(glob("projects")).filter((p) => !p.data.hidden).sort(sortByOrderThenName));

  eleventyConfig.addCollection("partners", (api) =>
    api.getFilteredByGlob(glob("partners")).filter((p) => !p.data.hidden).sort(sortByOrderThenName));

  eleventyConfig.addCollection("grants", (api) =>
    api.getFilteredByGlob(glob("grants")).filter((p) => !p.data.hidden)
      .sort((a, b) => (b.data.start_year ?? 0) - (a.data.start_year ?? 0) || sortByOrderThenName(a, b)));

  eleventyConfig.addCollection("datasets", (api) =>
    api.getFilteredByGlob(glob("datasets")).filter((p) => !p.data.hidden).sort(sortByOrderThenName));

  eleventyConfig.addCollection("news", (api) =>
    api.getFilteredByGlob(glob("news")).filter((p) => !p.data.draft).sort((a, b) => b.date - a.date));

  eleventyConfig.addCollection("publications", (api) =>
    api.getFilteredByGlob(glob("publications")).filter((p) => !p.data.hidden).sort((a, b) =>
      (b.data.year ?? 0) - (a.data.year ?? 0) ||
      STATUS_ORDER.indexOf(a.data.status ?? "published") - STATUS_ORDER.indexOf(b.data.status ?? "published") ||
      String(a.data.authors).localeCompare(String(b.data.authors))));

  // ---------- Filters ----------
  // Items tagged with a project slug, e.g. {{ collections.people | forProject("forever") }}
  eleventyConfig.addFilter("forProject", (items, slug) =>
    (items || []).filter((i) => (i.data.projects || []).includes(slug)));
  eleventyConfig.addFilter("where", (items, key, value) =>
    (items || []).filter((i) => (i.data ? i.data[key] : i[key]) === value));
  eleventyConfig.addFilter("whereIn", (items, key, values) =>
    (items || []).filter((i) => values.includes(i.data ? i.data[key] : i[key])));
  eleventyConfig.addFilter("whereNot", (items, key, value) =>
    (items || []).filter((i) => (i.data ? i.data[key] : i[key]) !== value));
  eleventyConfig.addFilter("limit", (arr, n) => (arr || []).slice(0, n));
  eleventyConfig.addFilter("isPeerReviewed", (items) =>
    (items || []).filter((i) => ["article", "review", "book-chapter", "proceedings"].includes(i.data.type) && (i.data.status ?? "published") === "published"));
  eleventyConfig.addFilter("findBySlug", (items, slug) => (items || []).find((i) => i.fileSlug === slug));
  eleventyConfig.addFilter("groupBy", (items, key) => {
    const groups = new Map();
    for (const i of items || []) {
      const k = i.data[key];
      if (!groups.has(k)) groups.set(k, []);
      groups.get(k).push(i);
    }
    return [...groups.entries()].map(([k, v]) => ({ key: k, items: v }));
  });
  eleventyConfig.addFilter("uniqueValues", (items, key) =>
    [...new Set((items || []).flatMap((i) => [].concat(i.data[key] ?? [])))].filter(Boolean));
  eleventyConfig.addFilter("date", (d, style = "long") => {
    if (!d) return "";
    const date = d instanceof Date ? d : new Date(d);
    const opts = style === "short" ? { month: "short", year: "numeric" } : { day: "numeric", month: "long", year: "numeric" };
    return date.toLocaleDateString("en-GB", { ...opts, timeZone: "UTC" });
  });
  eleventyConfig.addFilter("isoDate", (d) => (d ? new Date(d).toISOString().slice(0, 10) : ""));
  eleventyConfig.addFilter("initials", (name = "") => {
    const w = String(name).split(/\s+/).filter(Boolean);
    return ((w[0]?.[0] ?? "") + (w.length > 1 ? w[w.length - 1][0] : "")).toUpperCase();
  });
  eleventyConfig.addFilter("label", (value, map) => (map && map[value]) || value);
  eleventyConfig.addFilter("doiUrl", (doi) => (doi ? `https://doi.org/${String(doi).replace(/^https?:\/\/(dx\.)?doi\.org\//, "")}` : ""));
  eleventyConfig.addFilter("year", (d) => new Date(d).getUTCFullYear());
  eleventyConfig.addFilter("currentYear", () => new Date().getFullYear());
  eleventyConfig.addFilter("searchText", (data) =>
    [data.title, data.authors, data.venue, data.year, data.doi].filter(Boolean).join(" ").toLowerCase());
  eleventyConfig.addFilter("highlightAuthors", (authors, names) => {
    // Bold the group's own members in author lists (names come from site settings).
    let out = String(authors || "").replace(/&/g, "&amp;").replace(/</g, "&lt;");
    for (const n of names || []) out = out.split(n).join(`<strong>${n}</strong>`);
    return out;
  });

  return {
    dir: { input: "src", includes: "_includes", data: "_data", output: "_site" },
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk",
    // Set by the GitHub Pages workflow so links work at <org>.github.io/<repo>/
    pathPrefix: process.env.PATH_PREFIX || "/",
  };
}
