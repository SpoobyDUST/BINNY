#!/usr/bin/env node

var _passlint = require( '../passlint.js' )

var _fs = require( 'fs' )
var _path = require( 'path' )
var _pkg = require( '../package.json' )

var _glob = require( 'redstar' )

var argv = require( 'minimist' )( process.argv.slice( 2 ), {
  alias: {
    ecmaVersion: [ 'e', 'ev', 'ecma', 'ecmaversion', 'ecma-version' ],
    absolutePath: [ 'absolute-path', 'P' ],
    relativePath: [ 'path', 'p' ],
    version: [ 'V' ],
    help: [ 'h' ]
  },
  boolean: [ 'P', 'absolute-path', 'V', 'h' ]
} )

if ( argv.help ) {
  console.log(
    _fs.readFileSync(
      _path.join( __dirname, '../help.txt' ),
      'utf8'
    )
  )

  process.exit()
}

if ( argv.version ) {
  console.log(
    _pkg.name + ' version: ' + _pkg.version
  )

  process.exit()
}

if ( argv._.length <= 0 ) {
  console.error( 'Error! no files supplied - try `passlint **/*.js`' )
  process.exit( 1 )
  // argv._ = argv._.concat( require( 'glob' ).sync( '**/*.js' ) ) // default all js files
}

var buffer = ''
function checkFile ( file ) {
  var errline

  finish.counter = finish.counter || 0 // init
  finish.counter++ // increment

  try {
    var text = _fs.readFileSync( _path.resolve( file ), 'utf8' )

    var suffix = _path.extname( file )
    if ( suffix.toLowerCase().indexOf( 'css' ) >= 0 ) {
      errline = _passlint( text, 'css' )
    } else {
      errline = _passlint( text, argv.ecmaVersion )
    }
  } catch ( err ) {
    console.error( err.message.trim() )
    process.exit( 1 )
  }

  if ( argv.absolutePath ) {
    file = _path.resolve( file )
  } else {
    var dir = argv.relativePath ? _path.resolve( argv.relativePath ) : process.cwd()
    file = './' + _path.relative( dir, file )
  }

  if ( errline ) {
    // TODO wooster piping working
    buffer += ( '  ' + file + ':' + errline + '\n' )
  }

  clearTimeout( finish.timeout )
  finish.timeout = setTimeout( function () {
    // check for completion
    if ( finish.counter >= finish.endLimit ) {
      finish()
    }
  }, 0 )
}

finish.endLimit = finish.endLimit || 0 // init
argv._.forEach( function ( file ) {
  if ( _glob.hasMagic( file ) ) {
    var pattern = file

    file.endLimit++
    _glob( pattern, function ( err, files, dirs ) {
      if ( err ) throw err
      finish.counter++

      files.forEach( function ( file ) {
        finish.endLimit++
        checkFile( file )
      } )
    } )
  } else {
    finish.endLimit++
    checkFile( file )
  }
} )

function finish () {
  process.stderr.write( buffer )

  if ( buffer === '' ) {
    process.exit( 0 ) // no errors
  } else {
    process.exit( 1 )
  }
}
