var acorn = require( 'acorn' )

var csslint = require( 'csslint' )
var CSSLint = csslint.CSSLint

module.exports = passlint

function testjs ( text, ecmaVersion ) {
  var options = {
    ecmaVersion: ecmaVersion || 6
  }

  // ref: https://github.com/acornjs/acorn
  try {
    var ast = acorn.parse( text, options ) // eslint-disable-line
  } catch ( err ) {
    if ( err ) {
      try {
        /*
        * Attempt to get a fuller error description
        * ( usually the last line of err.toString() )
        */
        var string = String( err )
        if ( string ) {
          var split = string.split( '\n' )
          split.forEach( function ( str ) {
            var a = str.toLowerCase()
            var b = err.message.toLowerCase()
            if ( a.indexOf( b ) >= 0 ) {
              err.message = str
            }
          } )
        }
      } catch ( err ) { /* ignore */ }

      // add 'error' to the error message if it doesn't exist
      if ( err.message.toLowerCase().indexOf( 'error' ) === -1 ) {
        err.message = ( 'error: ' + err.message )
      }

      var loc = err.loc

      return (
        loc.line + ':' + loc.column + ': ' + err.message
      )
    }
  }

  return ''
}

function testcss ( text ) {
  var result = CSSLint.verify( text )
  var messages = result.messages
  var errors = messages.filter(
    function ( m ) { return m.type === 'error' }
  )

  var err = errors[ 0 ]

  if ( err ) {
    // add 'error' to the error message if it doesn't exist
    if ( err.message.toLowerCase().indexOf( 'error' ) === -1 ) {
      err.message = ( 'error: ' + err.message )
    }

    var loc = err

    return (
      loc.line + ':' + loc.col + ': ' + err.message
    )
  }

  return ''
}

function passlint ( text, opts ) {
  switch ( opts ) {
    case 'css':
    case 'style':
    case 'CSS':
      return testcss( text )
  }

  return testjs( text, opts )
}
