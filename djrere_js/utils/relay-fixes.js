export function fixObjKey(obj, key) {
  let hiddenKey = '_' + key;

  for(let objKey of Object.keys(obj)) {
    if (objKey.indexOf(hiddenKey) != -1) {
      obj[key] = obj[objKey];
      console.log('Fixing key ', objKey, " -> ", key );
      return
    }
  }

  //console.log('This object seems ok: ', obj);
}