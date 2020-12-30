function trimAllSpaces(val) {
  return val.trim().split(" ").join("");
}

function getAttr(selector, attrName) {
  var attrVal = selector.attr(attrName);
  if (attrVal) { return trimAllSpaces(attrVal); }
  return null;
}


function getTagName(el) {
  let selector = $(el);
  var attrVal = getAttr(selector, 'name');
  if (attrVal) {
    return attrVal;
  }
  attrVal = getAttr(selector, 'title');
  if (attrVal) {
    return attrVal;
  }
  attrVal = getAttr(selector, 'data-name');
  if (attrVal) {
    return attrVal;
  }
  if (selector.prop("tagName") == "DIV") {
    return null;
  }
  attrVal = selector.text();
  return trimAllSpaces(attrVal);
}

function addGtag(el, category, labelType) {
  let linkName = getTagName(el);
  if (!linkName) {
    return;
  }
  let selector = $(el);
  selector.attr('data-gtm-category', category);
  selector.attr('data-gtm-label', category + labelType + linkName);
}

function autoAddGtag(category, el) {
  $(el).find('a').each((index, item) => {
    addGtag(item, category, '_Link_');
  });
  $(el).find('button').each((index, item) => {
    addGtag(item, category, '_Btn_');
  });
  $(el).find('input').each((index, item) => {
    addGtag(item, category, '_Field_');
  });
  $(el).find('div').each((index, item) => {
    addGtag(item, category, '_Section_');
  });
  $(el).find('img').each((index, item) => {
    addGtag(item, category, '_Img_');
  });
  $(el).find('[allowfullscreen]').each(function (index, item) {
    addGtag(item, category, '_Video_');
  });
}