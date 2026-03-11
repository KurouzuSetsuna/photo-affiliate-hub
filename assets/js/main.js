// Photo Affiliate Hub - Main JS
document.addEventListener('DOMContentLoaded', function () {
  // 外部リンクに target="_blank" rel="noopener" を付与
  document.querySelectorAll('a[href^="http"]').forEach(function (link) {
    if (!link.rel.includes('noopener')) {
      link.setAttribute('rel', 'noopener noreferrer');
      link.setAttribute('target', '_blank');
    }
  });
});
