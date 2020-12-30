function() {
  return function(target, selector) {
    while (!target.matches(selector) && !target.matches('body')) {
      target = target.parentElement;
    }
    return target.matches(selector) ? target : undefined;
  }
}