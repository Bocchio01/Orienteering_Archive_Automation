const fs = require('fs')
const { Dropbox } = require('dropbox') // eslint-disable-line import/no-unresolved

const dbx = new Dropbox({
  accessToken: 'sl.BRvfuXa5zzEreoF44SVoian1y0YG_DpH39cRs3E9r3Co_t4QvJzgxEaggkYIYmEcLErtXqhwdEyw3z6W5ASSgz6AQMT8xfDUMqYuY6kNE3fRG2linPniVvoFbOjKIQeJIFDXnrA9',
})

dbx
  .filesDownload({ path: '/File di prova.html' })
  .then((res) => {
    console.log(res.result)
    let data = res.result

    fs.writeFile('.' + data.path_display, data.fileBinary, 'binary', (err) => {
      if (err) {
        throw err
      }
      console.log(`File: ${data.name} saved.`)
    })
  })
  .catch((err) => {
    throw err
  })
