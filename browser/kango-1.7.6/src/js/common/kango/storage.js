var utils=require("kango/utils"),array=utils.array,object=utils.object,EventTarget=utils.EventTarget,NotImplementedException=utils.NotImplementedException;function IStorage(){}IStorage.prototype={setItem:function(a,b){throw new NotImplementedException;},getItem:function(a){throw new NotImplementedException;},removeItem:function(a){throw new NotImplementedException;},getKeys:function(){throw new NotImplementedException;},clear:function(){throw new NotImplementedException;}};
function JSONStorage(a){EventTarget.call(this);this._storageEngine=a}
JSONStorage.prototype=object.extend(EventTarget,{_storageEngine:null,getItem:function(a){a=this._storageEngine.getItem(a);return"undefined"!=typeof a&&null!=a?JSON.parse(a):null},setItem:function(a,b){if("undefined"!=typeof b){var c=JSON.stringify(b);"undefined"!=typeof c&&(this._storageEngine.setItem(a,c),this.fireEvent("setItem",{data:{name:a,value:b}}))}else return this.removeItem(a);return!1},removeItem:function(a){this._storageEngine.removeItem(a);this.fireEvent("removeItem",{data:{name:a}})},
getKeys:function(){return this._storageEngine.getKeys()},getItems:function(){var a={};array.forEach(this.getKeys(),function(b){a[b]=this.getItem(b)},this);return a},clear:function(){this._storageEngine.clear();this.fireEvent("clear")},dispose:function(){this.removeAllEventListeners();"undefined"!=typeof this._storageEngine.dispose&&this._storageEngine.dispose();this._storageEngine=null}});function getPublicApi(){return utils.createApiWrapper(module.exports.storage,IStorage.prototype)};