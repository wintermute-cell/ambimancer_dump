import{S as A,i as G,s as J,I,k as p,q as w,a as S,l as g,m as v,r as y,h as i,c as P,n as F,b,G as k,J as q,K,B as C,L as H,p as M,u as U,e as R,M as x}from"../../chunks/index-d966ee31.js";const T=[["requestFullscreen","exitFullscreen","fullscreenElement","fullscreenEnabled","fullscreenchange","fullscreenerror"],["webkitRequestFullscreen","webkitExitFullscreen","webkitFullscreenElement","webkitFullscreenEnabled","webkitfullscreenchange","webkitfullscreenerror"],["webkitRequestFullScreen","webkitCancelFullScreen","webkitCurrentFullScreenElement","webkitCancelFullScreen","webkitfullscreenchange","webkitfullscreenerror"],["mozRequestFullScreen","mozCancelFullScreen","mozFullScreenElement","mozFullScreenEnabled","mozfullscreenchange","mozfullscreenerror"],["msRequestFullscreen","msExitFullscreen","msFullscreenElement","msFullscreenEnabled","MSFullscreenChange","MSFullscreenError"]],E=(()=>{if(typeof document>"u")return!1;const r=T[0],e={};for(const n of T)if((n==null?void 0:n[1])in document){for(const[l,c]of n.entries())e[r[l]]=c;return e}return!1})(),z={change:E.fullscreenchange,error:E.fullscreenerror};let m={request(r=document.documentElement,e){return new Promise((n,t)=>{const l=()=>{m.off("change",l),n()};m.on("change",l);const c=r[E.requestFullscreen](e);c instanceof Promise&&c.then(l).catch(t)})},exit(){return new Promise((r,e)=>{if(!m.isFullscreen){r();return}const n=()=>{m.off("change",n),r()};m.on("change",n);const t=document[E.exitFullscreen]();t instanceof Promise&&t.then(n).catch(e)})},toggle(r,e){return m.isFullscreen?m.exit():m.request(r,e)},onchange(r){m.on("change",r)},onerror(r){m.on("error",r)},on(r,e){const n=z[r];n&&document.addEventListener(n,e,!1)},off(r,e){const n=z[r];n&&document.removeEventListener(n,e,!1)},raw:E};Object.defineProperties(m,{isFullscreen:{get:()=>Boolean(document[E.fullscreenElement])},element:{enumerable:!0,get:()=>document[E.fullscreenElement]??void 0},isEnabled:{enumerable:!0,get:()=>Boolean(document[E.fullscreenEnabled])}});E||(m={isEnabled:!1});const $=m;function O(r,e,n){const t=r.slice();return t[5]=e[n],t}function V(r,e,n){const t=r.slice();return t[8]=e[n],t}function Q(r){let e,n=r[11].message+"",t;return{c(){e=p("p"),t=w(n),this.h()},l(l){e=g(l,"P",{style:!0});var c=v(e);t=y(c,n),c.forEach(i),this.h()},h(){M(e,"color","red")},m(l,c){b(l,e,c),k(e,t)},p(l,c){c&1&&n!==(n=l[11].message+"")&&U(t,n)},d(l){l&&i(e)}}}function W(r){let e,n=r[4][0],t=[];for(let l=0;l<n.length;l+=1)t[l]=L(O(r,n,l));return{c(){for(let l=0;l<t.length;l+=1)t[l].c();e=R()},l(l){for(let c=0;c<t.length;c+=1)t[c].l(l);e=R()},m(l,c){for(let s=0;s<t.length;s+=1)t[s].m(l,c);b(l,e,c)},p(l,c){if(c&1){n=l[4][0];let s;for(s=0;s<n.length;s+=1){const o=O(l,n,s);t[s]?t[s].p(o,c):(t[s]=L(o),t[s].c(),t[s].m(e.parentNode,e))}for(;s<t.length;s+=1)t[s].d(1);t.length=n.length}},d(l){x(t,l),l&&i(e)}}}function D(r){let e,n,t=r[4][1][r[8]].name+"",l,c,s,o;function d(){return r[3](r[8])}return{c(){e=p("button"),n=p("div"),l=w(t),c=S(),this.h()},l(a){e=g(a,"BUTTON",{class:!0,style:!0});var h=v(e);n=g(h,"DIV",{class:!0});var u=v(n);l=y(u,t),u.forEach(i),c=P(h),h.forEach(i),this.h()},h(){F(n,"class","button-name-wrapper svelte-rpystk"),F(e,"class","button svelte-rpystk"),M(e,"background-image","url('./get_icon?name="+r[4][1][r[8]].icon+"')")},m(a,h){b(a,e,h),k(e,n),k(n,l),k(e,c),s||(o=q(e,"click",d),s=!0)},p(a,h){r=a,h&1&&t!==(t=r[4][1][r[8]].name+"")&&U(l,t),h&1&&M(e,"background-image","url('./get_icon?name="+r[4][1][r[8]].icon+"')")},d(a){a&&i(e),s=!1,o()}}}function L(r){let e,n,t,l,c=r[5],s=[];for(let o=0;o<c.length;o+=1)s[o]=D(V(r,c,o));return{c(){e=p("section"),n=p("div"),t=p("div");for(let o=0;o<s.length;o+=1)s[o].c();l=S(),this.h()},l(o){e=g(o,"SECTION",{class:!0});var d=v(e);n=g(d,"DIV",{class:!0});var a=v(n);t=g(a,"DIV",{class:!0});var h=v(t);for(let u=0;u<s.length;u+=1)s[u].l(h);h.forEach(i),a.forEach(i),l=P(d),d.forEach(i),this.h()},h(){F(t,"class","button-container svelte-rpystk"),F(n,"class","page"),F(e,"class","svelte-rpystk")},m(o,d){b(o,e,d),k(e,n),k(n,t);for(let a=0;a<s.length;a+=1)s[a].m(t,null);k(e,l)},p(o,d){if(d&1){c=o[5];let a;for(a=0;a<c.length;a+=1){const h=V(o,c,a);s[a]?s[a].p(h,d):(s[a]=D(h),s[a].c(),s[a].m(t,null))}for(;a<s.length;a+=1)s[a].d(1);s.length=c.length}},d(o){o&&i(e),x(s,o)}}}function X(r){let e,n;return{c(){e=p("p"),n=w("waiting...")},l(t){e=g(t,"P",{});var l=v(e);n=y(l,"waiting..."),l.forEach(i)},m(t,l){b(t,e,l),k(e,n)},p:C,d(t){t&&i(e)}}}function Y(r){let e,n,t,l,c,s,o,d,a,h,u={ctx:r,current:null,token:null,hasCatch:!0,pending:X,then:W,catch:Q,value:4,error:11};return I(d=r[0],u),{c(){e=p("button"),n=w("F"),t=S(),l=p("button"),c=w("R"),s=S(),o=p("div"),u.block.c(),this.h()},l(f){e=g(f,"BUTTON",{});var _=v(e);n=y(_,"F"),_.forEach(i),t=P(f),l=g(f,"BUTTON",{});var N=v(l);c=y(N,"R"),N.forEach(i),s=P(f),o=g(f,"DIV",{id:!0,class:!0});var B=v(o);u.block.l(B),B.forEach(i),this.h()},h(){F(o,"id","container"),F(o,"class","svelte-rpystk")},m(f,_){b(f,e,_),k(e,n),b(f,t,_),b(f,l,_),k(l,c),b(f,s,_),b(f,o,_),u.block.m(o,u.anchor=null),u.mount=()=>o,u.anchor=null,a||(h=[q(e,"click",r[1]),q(l,"click",r[2])],a=!0)},p(f,[_]){r=f,u.ctx=r,_&1&&d!==(d=r[0])&&I(d,u)||K(u,r,_)},i:C,o:C,d(f){f&&i(e),f&&i(t),f&&i(l),f&&i(s),f&&i(o),u.block.d(),u.token=null,u=null,a=!1,H(h)}}}async function j(){const e=await(await fetch("./get_layout")).json(),t=await(await fetch("./get_buttons")).json();return[e,t]}function Z(r){fetch(`./run_button?name=${r}`)}function ee(r,e,n){let t=j();function l(){$.isEnabled&&$.toggle()}function c(){n(0,t=j())}return[t,l,c,o=>{Z(o)}]}class ne extends A{constructor(e){super(),G(this,e,ee,Y,J,{})}}export{ne as default};
