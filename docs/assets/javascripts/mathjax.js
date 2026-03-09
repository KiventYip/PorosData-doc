// docs/assets/javascripts/mathjax.js
window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
    processEscapes: true,
    processEnvironments: true
  },
  options: {
    // 配合 Material 主题，只解析指定 class 里的公式，提高全站渲染性能
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex"
  }
};