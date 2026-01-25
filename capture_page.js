/**
 * 使用 Puppeteer 将网页转换为完整长图
 */
const puppeteer = require('puppeteer');
const path = require('path');

async function captureFullPage(url, outputPath) {
    console.log('正在启动浏览器...');

    const browser = await puppeteer.launch({
        headless: 'new',
        executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const page = await browser.newPage();

    // 设置视口宽度
    await page.setViewport({
        width: 800,
        height: 1200,
        deviceScaleFactor: 2  // 2倍分辨率，更清晰
    });

    console.log(`正在打开页面: ${url}`);
    await page.goto(url, {
        waitUntil: 'networkidle2',
        timeout: 60000
    });

    // 等待图片加载
    console.log('等待页面资源加载完成...');
    await new Promise(r => setTimeout(r, 3000));

    // 移除可能的焦点边框
    await page.addStyleTag({
        content: `
            * {
                outline: none !important;
            }
        `
    });

    console.log('正在截取完整页面...');
    await page.screenshot({
        path: outputPath,
        fullPage: true,
        type: 'png'
    });

    console.log(`✅ 截图已保存到: ${outputPath}`);

    await browser.close();
}

// 主函数
const url = process.argv[2] || 'http://localhost:3000/archives-260119/ai_posts_summary_2026-01-19.html';
const outputPath = process.argv[3] || 'archives-260119/ai_posts_summary_2026-01-19_full_page.png';

captureFullPage(url, outputPath)
    .then(() => console.log('✅ 完成！'))
    .catch(err => {
        console.error('❌ 错误:', err.message);
        process.exit(1);
    });
