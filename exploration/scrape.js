const axios = require('axios');
const { time } = require('console');
const fs = require('fs');


// const chars = ""
const chars = "abcdefghijklmnopqrstuvwxyz"
const categories = [...chars.split(''), '19']



function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// copied from https://stackoverflow.com/questions/494143/creating-a-new-dom-element-from-an-html-string-using-built-in-dom-methods-or-pro
function createElementFromHTML(htmlString) {
    var div = createElement('div');
    div.innerHTML = htmlString.trim();

    return div.firstChild;
}



const main = async () => {
    for (let c of categories) {
        axios.get(`https://www.azlyrics.com/${c}.html`)
            .then(res => {
                // const ashtml = createElementFromHTML(res.data);
                // const artists = [...ashtml.querySelector(".container.main-page").querySelectorAll("a")].map(x => x.innerText).join(",")
                fs.writeFile(`./scrapedpages/${c}.html`, res.data, err => {
                    if (err) {
                        console.error(err);
                    }
                });
            })
            .catch(err => {
                console.log('Error: ', err.message);
            });
        await sleep(3000);
    }
}

const d = {}

for (let c of categories) {
    const data = fs.readFileSync(`./scrapedpages/${c}.html`, 'utf8')
    const match = data.match(/(?<=html">)(.+)(?=<\/a><br>)/g);
    for (let artist of match) {
        d[artist] = false;
    }
}

// console.log(d)

// console.log(JSON.stringify(d, null, 2))

fs.writeFileSync('./artists.json', JSON.stringify(d, null, 4), 'utf-8');