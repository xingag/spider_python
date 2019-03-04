//简书上的文章保存为pdf保存到本地
const puppeteer = require('puppeteer');

const mkdirp = require('mkdirp');

BASE_URL = 'https://www.jianshu.com';

HOME_URL = `${BASE_URL}/u/f46becd1ed83`;

//文章目录
const ARTICLE_PATH = './monkey';

const download_article = async () => {

    const viewport_size = {
        width: 0,
        height: 0,
    };

    const browser = await puppeteer.launch({
        headless: true,
    });

    const page = await browser.newPage();

    page.setViewport(viewport_size);

    //打开文章主页
    await page.goto(HOME_URL);

    console.log('显示文章列表，马上开始滑动')

    //滑动文章列表，使所有文章被加载出来
    //参考：https://github.com/GoogleChrome/puppeteer/issues/844
    await autoScroll(page);

    console.log('所有文章加载完成');

    const articles = await page.$eval('.note-list', articles_element => {
        const article_elements = articles_element.querySelectorAll('li');
        const articleElementArray = Array.prototype.slice.call(article_elements);

        return articleElementArray.map(item => {
            const a_element = item.querySelector('.title');
            return {
                href: a_element.getAttribute('href'),
                title: a_element.innerHTML.trim(),
            };
        });
    });

    console.log(`大佬一共发布了${articles.length}篇文章`);


    //新建目录
    mkdirp.sync(ARTICLE_PATH);

    for (let article of articles) {
        const articlePage = await browser.newPage();
        articlePage.setViewport(viewport_size);
        articlePage.goto(`${BASE_URL}${article.href}`, {
            waitUntil: 'networkidle2'
        });

        articlePage.waitForSelector('.post');
        console.log('文章详情页面加载完成');

        //注意：这里必须等待几秒，不然下面的滑动会报错：
        // UnhandledPromiseRejectionWarning: Error: Execution context was destroyed, most likely because of a navigation.
        await articlePage.waitFor(2000);

        //滑动到最底部，加载出所有的图片
        await autoScroll(articlePage);


        //为了保证页面的整洁干净，屏蔽多余的元素
        await articlePage.$eval('body', body => {
            body.querySelector('.navbar').style.display = 'none';
            body.querySelector('#note-fixed-ad-container').style.display = 'none';
            body.querySelector('.note-bottom').style.display = 'none';
            body.querySelector('.side-tool').style.display = 'none';
            // body.querySelector('.author').style.display = 'none';
            body.querySelector('.meta-bottom').style.display = 'none';
            body.querySelector('#web-note-ad-1').style.display = 'none';
            body.querySelector('#comment-list').style.display = 'none';
            body.querySelector('.follow-detail').style.display = 'none';
            body.querySelector('.show-foot').style.display = 'none';

            Promise.resolve();
        });

        //文章名称
        const fileName = `${article.title.replace("/\\//g", "、")}.pdf`;
        const fileFullPath = `${ARTICLE_PATH}/${fileName}`;
        console.log(`文章保存的完整路径是:${fileFullPath}`);

        await page.emulateMedia('screen');
        await articlePage.pdf({
            path: fileFullPath,
            format: 'A4'
        });
        console.log(`保存成功: ${fileFullPath}`);
        articlePage.close();
    }

    console.log('下载完成！Enjoy~');
};

function autoScroll(page) {
    return page.evaluate(() => {
        return new Promise((resolve, reject) => {
            var totalHeight = 0;
            var distance = 100;
            var timer = setInterval(() => {
                console.log('执行间断函数');
                var scrollHeight = document.body.scrollHeight;
                window.scrollBy(0, distance);
                totalHeight += distance;

                if (totalHeight >= scrollHeight) {
                    console.log('滑动到底');
                    clearInterval(timer);
                    resolve();
                }
            }, 100);
        })
    });
}


module.exports = download_article;

if (require.main === module) {
    download_article()
}


