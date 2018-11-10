// Patch for Vue.js to enable djangoCMS's "double click to edit" feature.
//
// To set it up you should call `new VueDjangoCMSPatch(this)` in a `created`
// hook on a Vue instance.
// And add 'cms-template' and 'cms-plugin' to `Vue.config.ignoredElements`.


var VueDjangoCMSPatch = function (instance) {
  this.instance = instance;

  this._canBePatched = function () {
    return window.CMS !== undefined && window.CMS.config.mode === 'draft';
  };

  this._replaceTemplateTags = function () {
    var templates = document.querySelectorAll('template.cms-plugin');
    for (var i = 0; i < templates.length; i++) {
      var template = templates[i];
      var cmsTemplate = document.createElement('cms-template');
      cmsTemplate.className = template.className;
      template.parentNode.insertBefore(cmsTemplate, template);
      template.parentNode.removeChild(template);
    }
  };

  this._moveScriptTags = function () {
    var scripts = document.querySelectorAll(this.instance.$options.el + ' script[data-cms]');
    for (var i = 0; i < scripts.length; i++) {
      scripts[i].parentNode.removeChild(scripts[i]);
      document.body.appendChild(scripts[i]);
    }
  };

  this._cleanTemplateTags = function () {
    var cmsTemplates = document.querySelectorAll('cms-template');
    for (var i = 0; i < cmsTemplates.length; i++) {
      cmsTemplates[i].parentNode.removeChild(cmsTemplates[i]);
    }
  };

  this.refresh = function () {
    if (this._canBePatched()) {
      this.instance.$destroy();
      delete this.instance.$options.render;  // Force re-render.
      this.instance = new this.instance.constructor(this.instance.$options);
      window.CMS.Plugin._initializeTree();
    }
  };

  this.patch = function () {
    if (this._canBePatched()) {
      this._replaceTemplateTags();
      this._moveScriptTags();
      window.CMS.$(document).on('ready', this._cleanTemplateTags.bind(this));
      window.CMS.$(window).on('cms-content-refresh', this.refresh.bind(this));
    }
  };

  this.init = function () {
    if (this._canBePatched() && !this.instance.$options._cmsPatched) {
      window.console.log('Vue DjangoCMS patch initialized.');
      this.patch();
      this.instance.$options._cmsPatched = true;
    }
  };

  this.init();
};

export { VueDjangoCMSPatch as default }
