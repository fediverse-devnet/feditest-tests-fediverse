/*
 * ANNOtate your Spec with Tests (ANNO-S-T).
 * Experimental :-)
 */

// A test
class AnnostTest extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this.shadowRoot.innerHTML = `
      <link rel='stylesheet' href='annost.css'>
      <section class='annost annost-test'>
        <div class='annost-bar'>ANNOST TEST</div>
        <div class='annost-content'>
          <h2></h2>
          <slot></slot>
        </div>
      </section>
    `;
  }

  static get observedAttributes() {
    return ['testid', 'testname', 'testlevel', 'testrole'];
  }

  attributeChangedCallback(name, oldValue, newValue) {
    var label =  this.getAttribute('role') + ' Test ' + this.getAttribute('testid');
    if( this.getAttribute('name') !== '' ) {
        label += ": " + this.getAttribute('name');
    }
    label += ' (' + this.getAttribute('level') + ')';
    this.shadowRoot.querySelector('h2').textContent = label;

    this.id = 'test-' + this.getAttribute('testid');
  }
}

// A cross-reference to a test defined elsewhere
class AnnostCrossRef extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this.shadowRoot.innerHTML = `
      <link rel='stylesheet' href='annost.css'>
      <section class='annost annost-xref'>
        <div class='annost-bar'>ANNOST XREF</div>
        <div class='annost-content'>
          <h3></h3>
          <slot></slot>
        </div>
      </section>
    `;
  }

  static get observedAttributes() {
    return ['target'];
  }

  attributeChangedCallback(name, oldValue, newValue) {
    var link = document.createElement('a');
    link.setAttribute('href', '#test-' + this.getAttribute('target'));
    link.textContent = 'See Test ' + this.getAttribute('target');

    var label = 'See ' + this.getAttribute('target')
    this.shadowRoot.querySelector('h3').replaceChildren(link);
  }
}

// A note
class AnnostNote extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this.shadowRoot.innerHTML = `
      <link rel='stylesheet' href='annost.css'>
      <section class='annost annost-note'>
        <div class='annost-bar'>ANNOST NOTE</div>
        <div class='annost-content'>
          <h3>Note</h3>
          <slot></slot>
        </div>
      </section>
    `;
  }
}

customElements.define('annost-test', AnnostTest);
customElements.define('annost-xref', AnnostCrossRef);
customElements.define('annost-note', AnnostNote);

document.addEventListener('DOMContentLoaded', function(event){
  const already = document.findElementById('annost-title');
  if( already === null ) {
    const disclaimer = document.createElement('h1');
    disclaimer.id = 'annost-title';
    disclaimer.style = 'display: block; text-align: left; color: #c04040; padding: 20px; border: 1px solid #c04040; font-family: Arial';
    disclaimer.innerHTML = 'Annotated by <a href="https://github.com/jernst/annost/">AnnoST</a>. Experimental :-)';
    document.getElementsByTagName('body')[0].prepend( disclaimer );
  }
});
