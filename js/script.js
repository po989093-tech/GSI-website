// Basic interactivity: mobile nav toggle and reveal-on-scroll
document.addEventListener('DOMContentLoaded', function(){
  const navToggle = document.querySelector('.nav-toggle');
  const siteNav = document.querySelector('.site-nav');
  navToggle && navToggle.addEventListener('click', function(){
    const isExpanded = this.getAttribute('aria-expanded') === 'true';
    this.setAttribute('aria-expanded', String(!isExpanded));
    siteNav && siteNav.classList.toggle('show');
  });

  // simple reveal on scroll
  const observer = new IntersectionObserver((entries)=>{
    entries.forEach(e=>{
      if(e.isIntersecting){
        e.target.classList.add('visible');
        observer.unobserve(e.target);
      }
    })
  },{threshold:0.08});

  document.querySelectorAll('.card, .project-card, .programme-card').forEach(el=>observer.observe(el));

  // contact form basic client-side validation (non-blocking)
  const form = document.getElementById('contact-form');
  if(form){
    form.addEventListener('submit', function(e){
      e.preventDefault();
      alert('This form is a placeholder. Configure server-side handling or integrate an email service.');
    });
  }

  // Remove <source> entries that point to missing optimized images to avoid 404 fetches
  async function pruneMissingOptimizedSources(){
    const sources = Array.from(document.querySelectorAll('picture source'));
    await Promise.all(sources.map(async (s)=>{
      const src = s.getAttribute('srcset');
      if(!src || !src.includes('/images/optimized/')) return;
      try{
        const res = await fetch(src, {method:'GET'});
        if(!res.ok){
          s.remove();
        }
      }catch(err){
        s.remove();
      }
    }));
  }
  pruneMissingOptimizedSources();
});