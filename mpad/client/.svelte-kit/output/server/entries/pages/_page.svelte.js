import { c as create_ssr_component, i as is_promise, n as noop, d as each, e as escape } from "../../chunks/index.js";
import "screenfull";
const _page_svelte_svelte_type_style_lang = "";
const css = {
  code: ":root{--fg_primary:#fffefd;--fg_secondary:#E1BB80;--fg_tertiary:#7B6B43;--bg_primary:#121217;--bg_secondary:#7765E3;--bg_tertiary:#806443}body{margin:0;overflow-x:hidden;overflow-y:hidden}#container.svelte-rpystk{background-color:var(--bg_primary);display:flex;overflow-x:scroll;scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch}section.svelte-rpystk{border-right:1px solid white;padding:1rem;min-width:100vw;height:100vh;scroll-snap-align:start;text-align:center;position:relative}.button-container.svelte-rpystk{display:flex;flex-wrap:wrap;flex-direction:row;justify-content:left}.button.svelte-rpystk{position:relative;display:inline-block;color:var(--fg_primary);width:128px;height:128px;max-width:128px;max-height:128px;margin:20px;font-weight:1000;font-size:1.1em;padding:0;font-family:Verdana, Arial, sans-serif;border-radius:40px;box-shadow:3px 4px #1f1d24,15px 15px 30px #000000e6;transition:all .3s;outline:none;border:2px solid #443f3f}.button.svelte-rpystk:active{transform:translate(4px, 5px);box-shadow:none}.button-name-wrapper.svelte-rpystk{display:flex;align-items:flex-end;justify-content:center;background:linear-gradient(to top, rgba(10, 10, 10, 0.6) 0% 28%, transparent 56% 55%);text-shadow:-1px -1px 0 #242424, 1px -1px 0 #242424, -1px 1px 0 #242424, 1px 1px 0 #242424;height:100%;width:100%;padding:4px;box-sizing:border-box;border-radius:36px}",
  map: null
};
async function fetchLayout() {
  const layout_response = await fetch("./get_layout");
  const layout = await layout_response.json();
  const buttons_response = await fetch("./get_buttons");
  const buttons = await buttons_response.json();
  return [layout, buttons];
}
const Page = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let fetchedLayout = fetchLayout();
  $$result.css.add(css);
  return `<button>F</button>
<button>R</button>
<div id="${"container"}" class="${"svelte-rpystk"}">${function(__value) {
    if (is_promise(__value)) {
      __value.then(null, noop);
      return `
        <p>waiting...</p>
    `;
    }
    return function(data) {
      return `
        ${each(data[0], (page) => {
        return `<section class="${"svelte-rpystk"}"><div class="${"page"}"><div class="${"button-container svelte-rpystk"}">${each(page, (button_name) => {
          return `<button class="${"button svelte-rpystk"}" style="${"background-image: url('./get_icon?name=" + escape(data[1][button_name]["icon"], true) + "');"}"><div class="${"button-name-wrapper svelte-rpystk"}">${escape(data[1][button_name]["name"])}</div>
                            </button>`;
        })}
                    </div></div>
            </section>`;
      })}
    `;
    }(__value);
  }(fetchedLayout)}
</div>`;
});
export {
  Page as default
};
