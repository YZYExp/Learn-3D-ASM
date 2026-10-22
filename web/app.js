'use strict';
const chapters = window.BOOK_CHAPTERS;
const $ = id => document.getElementById(id);
const groups = [
 {number:'00', title:'先翻开这本书', description:'了解读法与图像标识', ids:['00']},
 {number:'01', title:'认识制造的原理', description:'发展、分类与主要打印工艺', ids:['01','02','03','04','05','06']},
 {number:'02', title:'走近材料与设计', description:'从模型到成品，读懂制造的取舍', ids:['07','08','09','10','11']},
 {number:'03', title:'认识品牌与造物者', description:'当代生态、团队故事与观察练习', ids:['12','13','14','15','16']},
 {number:'04', title:'随时回来查一查', description:'术语、缩写与延伸阅读', ids:['17']}
];
const plainTitle = ch => ch.title.replace(/^\d{2}\s+/, '');
const esc = str => str.replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
const remember = (key,value) => { try { localStorage.setItem(key,value); } catch {} };
const recall = key => { try { return localStorage.getItem(key); } catch { return null; } };
let current = null;

function drawDirectory(query='') {
 const q=query.trim().toLocaleLowerCase();let count=0;
 $('chapter-groups').innerHTML=groups.map(group=>{
  const matches=group.ids.map(id=>chapters.find(ch=>ch.id===id)).filter(ch=>!q || (ch.title+' '+ch.summary+' '+ch.search).toLocaleLowerCase().includes(q));
  count+=matches.length;if(!matches.length)return '';
  return `<section class="chapter-group"><div class="group-name"><span>${group.number}</span><h3>${group.title}</h3><p>${group.description}</p></div><div>${matches.map(ch=>`<a class="chapter-row" href="#read/${ch.id}"><span class="chapter-number">${ch.id==='00'?'导读':ch.id==='17'?'附录':ch.id}</span><div><h4>${esc(plainTitle(ch))}</h4><p>${esc(ch.summary)}</p></div><span aria-hidden="true">↗</span></a>`).join('')}</div></section>`;
 }).join('');
 $('empty-search').hidden=count>0;
 $('search-count').textContent=q?`找到 ${count} 个相关章节`:'按顺序阅读，或从感兴趣的一章开始。';
}

function setDrawer(open) {
 document.body.classList.toggle('drawer-open',open);
 $('mobile-toc').setAttribute('aria-expanded',String(open));
 $('drawer-shade').hidden=!open;
}

function render() {
 const match=location.hash.match(/^#read\/(\d{2})$/);
 const ch=match && chapters.find(c=>c.id===match[1]);
 if(!ch){
  current=null;document.body.classList.remove('reading');$('reader-view').hidden=true;$('home-view').hidden=false;setDrawer(false);
  document.title='造物的加减法 · 3D打印与制造图鉴';
  const target=location.hash.slice(1);
  requestAnimationFrame(()=>{if(target && $(target))$(target).scrollIntoView();else window.scrollTo(0,0);});
  refreshResume();return;
 }
 current=ch;document.body.classList.add('reading');$('home-view').hidden=true;$('reader-view').hidden=false;setDrawer(false);
 $('reader-title').textContent=plainTitle(ch);
 $('reader-kicker').textContent=ch.id==='00'?'BEFORE WE BEGIN / 导读':ch.id==='17'?'KEEP EXPLORING / 附录':`CHAPTER ${ch.id} / 造物的加减法`;
 $('reader-summary').textContent=ch.summary;
 $('chapter-content').innerHTML=ch.html;
 $('chapter-pdf').href=`pdf/chapters/${ch.id}.pdf`;
 $('chapter-source').href=`chapters/${ch.id}.md`;
 $('chapter-source').target='_blank';$('chapter-source').rel='noopener';
 $('reader-nav').innerHTML=chapters.map(c=>`<a href="#read/${c.id}" ${c.id===ch.id?'aria-current="page"':''}><span>${c.id==='00'?'序':c.id==='17'?'附':c.id}</span>${esc(plainTitle(c))}</a>`).join('');
 const i=chapters.indexOf(ch),prev=chapters[i-1],next=chapters[i+1];
 $('chapter-pager').innerHTML=(prev?`<a href="#read/${prev.id}"><span>← 上一章</span>${esc(plainTitle(prev))}</a>`:'')+(next?`<a href="#read/${next.id}"><span>下一章 →</span>${esc(plainTitle(next))}</a>`:'<a href="#chapters"><span>全书阅读完成</span>返回全书目录 ↗</a>');
 document.title=`${plainTitle(ch)} · 造物的加减法`;
 remember('manufacturing-atlas-last',ch.id);
 requestAnimationFrame(()=>{window.scrollTo(0,0);updateProgress();});
}

function refreshResume(){const id=recall('manufacturing-atlas-last'),ch=chapters.find(c=>c.id===id);$('resume-link').hidden=!ch;if(ch){$('resume-link').href=`#read/${ch.id}`;$('resume-link').textContent=`继续阅读：${plainTitle(ch)} →`;}}
function updateProgress(){if(!current)return;const total=document.documentElement.scrollHeight-window.innerHeight;const value=total>0?Math.max(0,Math.min(100,window.scrollY/total*100)):100;$('reading-progress-bar').style.width=value+'%';}
function openImage(img){$('expanded-image').src=img.src;$('expanded-image').alt=img.alt;$('image-dialog-caption').textContent=img.alt;$('image-dialog').showModal();$('close-image').focus();}

$('home-search').addEventListener('input',e=>drawDirectory(e.target.value));
$('mobile-toc').addEventListener('click',()=>setDrawer(!document.body.classList.contains('drawer-open')));
$('drawer-shade').addEventListener('click',()=>setDrawer(false));
$('font-size').addEventListener('click',()=>{const large=document.body.classList.toggle('large-type');$('font-size').setAttribute('aria-pressed',String(large));remember('manufacturing-atlas-large',String(large));});
$('close-image').addEventListener('click',()=>$('image-dialog').close());
$('image-dialog').addEventListener('click',e=>{if(e.target===$('image-dialog'))$('image-dialog').close();});
document.addEventListener('click',e=>{const img=e.target.closest('.book-prose img,.comparison-image img');if(img)openImage(img);});
document.addEventListener('keydown',e=>{
 if(e.key==='Escape')setDrawer(false);
 if(e.key==='/' && !current && !['INPUT','TEXTAREA'].includes(document.activeElement.tagName)){e.preventDefault();$('home-search').focus();$('home-search').scrollIntoView({block:'center'});}
 if((e.key==='Enter'||e.key===' ') && e.target.matches('.book-prose img,.comparison-image img')){e.preventDefault();openImage(e.target);}
});
window.addEventListener('hashchange',render);
window.addEventListener('scroll',updateProgress,{passive:true});window.addEventListener('resize',updateProgress);
const large=recall('manufacturing-atlas-large')==='true';document.body.classList.toggle('large-type',large);$('font-size').setAttribute('aria-pressed',String(large));
// Make a network failure visible instead of leaving an empty image panel.
function imageFailure(img){
 if(img.dataset.failed || !img.getAttribute('src'))return;
 img.dataset.failed='true';
 const retry=document.createElement('button');
 retry.type='button';retry.className='image-retry';
 retry.textContent='图片未加载，点击重试 ↻';
 retry.addEventListener('click',e=>{
  e.preventDefault();e.stopPropagation();
  const src=img.getAttribute('src');
  delete img.dataset.failed;retry.remove();
  const url=new URL(src,document.baseURI);url.searchParams.set('retry',Date.now());
  img.src=url.href;
 });
 img.after(retry);
}
document.addEventListener('error',e=>{if(e.target instanceof HTMLImageElement)imageFailure(e.target);},true);
document.querySelectorAll('img[src]').forEach(img=>{if(img.complete && !img.naturalWidth)imageFailure(img);});
drawDirectory();refreshResume();render();
