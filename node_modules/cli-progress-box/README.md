![](https://i.imgur.com/xFMQ3Y3.gif)

[![npm](https://img.shields.io/npm/v/cli-progress-box.svg?maxAge=3600&style=flat-square)](https://www.npmjs.com/package/cli-progress-box)
[![npm](https://img.shields.io/npm/l/cli-progress-box.svg?maxAge=3600&style=flat-square)](https://github.com/talmobi/cli-progress-box/blob/master/LICENSE)

# cli-progress-box
Quick visual change detection indicator

## Easy to use

#### Usage
```javascript
var opts = { padding: 2, maxStep: 8, width: 3 }
var box = require( 'cli-progress-box' )( opts )

opts.character = '愛'

setInterval( function () {
  opts.clcColor = box.bgColors.bright[ opts.step ]
  console.log( box.clc.reset + box.tick() )
}, 200 )
```

###### output
![](https://i.imgur.com/IsBnNfh.gif)

## About
A visual CLI change/progress indicator

## Why
When you save a file and your watcher rebuilds your project it is sometimes
hard to see that anything has changed because the output from the watch process is
so similar to the previous output.

## For who?
CLI applications.

## How
[cli-color](https://github.com/medikoo/cli-color)

## API
```javascript
var progressBox = require( 'cli-progress-box' )

var opts = {} // state object ( mutates )
var box = progressBox( opts ) // create new progress box

box.tick() // alias for box()
box.redraw() // shorthand for `box.clc.reset + box.tick()`

box.clc // embedded `medikoo/cli-color` object

box.bgColors.dark // list of `medikoo/cli-color` bacground colors
box.bgColors.bright // list of bright `medikoo/cli-color` background colors
box.bgColors.all // both lists

box.fgColors.dark // list of `medikoo/cli-color` bacground colors
box.fgColors.bright // list of bright `medikoo/cli-color` background colors
box.fgColors.all // both lists
```

## Options / Initial State
```
opts = opts || {}

if ( !opts.step ) opts.step = 0
if ( !opts.maxStep ) opts.maxStep = 4

if ( !opts.offset ) opts.offset = 0
if ( !opts.width ) opts.width = 2
if ( !opts.stepSize ) opts.stepSize = opts.stepSize

if ( !opts.padding ) opts.padding = 0
if ( !opts.margin ) opts.margin = 4

if ( !opts.character ) opts.character = ' '
if ( !opts.colors ) opts.colors = clcBgColors.bright.slice() // color changes based on opts.step

if ( !opts.getHeader ) opts.getHeader = function ( opts ) { return '' }
if ( !opts.getFooter ) opts.getFooter = function ( opts ) { return '' }

if ( !opts.transform ) opts.transform = _transform
if ( !opts.render ) opts.render = _render
if ( !opts.generateBox ) opts.generateBox = _generateBox
```

## Alternatives

## Test
```
npm test
```
