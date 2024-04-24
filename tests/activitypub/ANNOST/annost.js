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
      <section style="margin: 20px 0; padding: 20px; border: 1px solid #c04040; font-family: Arial;">
        <p style="margin: 0; font-weight: 700"></p>
        <h2 style="margin-top: 0"></h2>
        <slot></slot>
      </section>
    `;
  }

  static get observedAttributes() {
    return ['testid', 'testname', 'testlevel', 'testrole'];
  }

  attributeChangedCallback(name, oldValue, newValue) {
    var roleLabel =  this.getAttribute('role');
    roleLabel = roleLabel.indexOf(',') > 0 ? ( "Roles: " + roleLabel ) : ( "Role:" + roleLabel );
    var mainLabel =  "Test " + this.getAttribute('testid');
    if( this.getAttribute( 'name') !== '' ) {
        mainLabel += ": " + this.getAttribute('name');
    }
    mainLabel += ' (' + this.getAttribute('level') + ')';
    this.shadowRoot.querySelector('p').textContent = roleLabel;
    this.shadowRoot.querySelector('h2').textContent = mainLabel;

    this.id = "test-" + this.getAttribute('testid');
  }
}

// A cross-reference to a test defined elsewhere
class AnnostCrossRef extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this.shadowRoot.innerHTML = `
      <section style="margin: 20px 0; padding: 20px; border: 1px solid #c04040; font-family: Arial">
        <h3 style="margin-top: 0"></h3>
        <slot></slot>
      </section>
    `;
  }

  static get observedAttributes() {
    return ['target'];
  }

  attributeChangedCallback(name, oldValue, newValue) {
    var link = document.createElement( 'a' );
    link.setAttribute( 'href', "#test-" + this.getAttribute('target'));
    link.textContent = "See Test " + this.getAttribute('target');

    var label = "See " + this.getAttribute('target')
    this.shadowRoot.querySelector('h3').replaceChildren( link );
  }
}

// A note
class AnnostNote extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this.shadowRoot.innerHTML = `
      <section style="margin: 20px 0; padding: 20px; border: 1px solid #c04040; font-family: Arial">
        <h3 style="margin-top: 0">Note</h3>
        <slot></slot>
      </section>
    `;
  }
}

customElements.define('annost-test', AnnostTest);
customElements.define('annost-xref', AnnostCrossRef);
customElements.define('annost-note', AnnostNote);

document.addEventListener("DOMContentLoaded", function(event){
  const already = document.findElementById( 'annost-title');
  if( already === null ) {
    const disclaimer = document.createElement( 'h1' );
    disclaimer.id = 'annost-title';
    disclaimer.style = 'display: block; text-align: left; color: #c04040; padding: 20px; border: 1px solid #c04040; font-family: Arial';
    disclaimer.innerHTML = "Annotated by AnnoST. Experimental :-)";
    document.getElementsByTagName( 'body' )[0].prepend( disclaimer );
  }
});
