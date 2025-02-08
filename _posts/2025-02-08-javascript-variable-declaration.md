---
layout: post
author: Kyo
title: "JavaScript 變數宣告的重要觀念：let、var 與 const"
image: 
featured: false
categories: TechNotes JavaScript
---

在 JavaScript 中，變數宣告的方式有 `var`、`let` 和 `const` 三種。這些宣告方式看似類似，但實際上有很大的差異。今天讓我們深入了解這些重要的觀念。

## 作用域 (Scope) 的差異

`var` 是函式作用域 (function-scoped)，而 `let` 和 `const` 是區塊作用域 (block-scoped)。

```javascript
function scopeTest() {
    var x = 1;
    let y = 2;
    
    if (true) {
        var x = 3;    // 同一個 x
        let y = 4;    // 新的 y
        console.log(x, y);  // 3, 4
    }
    
    console.log(x, y);  // 3, 2
}
```

## 變量提升 (Hoisting)

`var` 宣告會被提升到作用域的頂部，但初始化不會。而 `let` 和 `const` 不會被提升。

```javascript
console.log(x);  // undefined
console.log(y);  // ReferenceError: y is not defined

var x = 1;
let y = 2;
```

## for 迴圈中的綁定差異

`let` 在每次迭代都會創建新的綁定，這在非同步操作中特別有用：

```javascript
// 使用 var
for (var i = 0; i < 3; i++) {
    setTimeout(() => console.log(i), 100);
}
// 輸出: 3, 3, 3

// 使用 let
for (let i = 0; i < 3; i++) {
    setTimeout(() => console.log(i), 100);
}
// 輸出: 0, 1, 2
```

## 重複宣告

`var` 允許重複宣告同一個變數，而 `let` 和 `const` 不允許：

```javascript
var x = 1;
var x = 2;  // 允許

let y = 1;
let y = 2;  // SyntaxError: Identifier 'y' has already been declared

const z = 1;
const z = 2;  // SyntaxError: Identifier 'z' has already been declared
```

## const 的特別之處

`const` 宣告的變數不能被重新賦值，但如果是物件，其屬性仍然可以修改：

```javascript
const user = {
    name: 'John'
};

user.name = 'Jane';  // 允許
console.log(user.name);  // Jane

user = {};  // TypeError: Assignment to constant variable
```

## 最佳實踐建議

1. 預設使用 `const`
2. 需要重新賦值時使用 `let`
3. 避免使用 `var`（除非需要支援舊版瀏覽器）

這樣的使用方式可以：
- 避免意外改變變數值
- 讓程式碼更容易理解和維護
- 減少 bug 發生的機會

## 總結

了解這些變數宣告的差異對於寫出優質的 JavaScript 程式碼非常重要。建議在現代 JavaScript 開發中，優先使用 `const` 和 `let`，這樣可以避免很多常見的問題，讓程式碼更加可靠和易於維護。 