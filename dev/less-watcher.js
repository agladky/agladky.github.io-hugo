const fs = require('fs');
const spawn = require('child_process').spawn;

process.argv.slice(2).forEach(function(file) {
  fs.watch(file, function(e) {
    console.log(e);
    if (e === 'change') {
      let ls = spawn('lessc', ['./less/main.less', '../static/css/main.css']);

      ls.stdout.on('data', (data) => {
        console.log(`stdout: ${data}`);
      });

      ls.stderr.on('data', (data) => {
        console.log(`stderr: ${data}`);
      });
    }
  });
});
