const fs = require('fs');
const path = require('path');
const svgstore = require('svgstore');
const sprites = svgstore();

const ICONS_DIR = path.join(__dirname, '../public/icons'); // SVG文件所在目录
const SPRITE_PATH = path.join(__dirname, '../public/sprite.svg'); // 输出的sprite文件路径

// 确保目录存在
if (!fs.existsSync(ICONS_DIR)) {
    fs.mkdirSync(ICONS_DIR, { recursive: true });
}

// 读取所有SVG文件
fs.readdirSync(ICONS_DIR)
    .filter(file => path.extname(file) === '.svg')
    .forEach(file => {
        const filepath = path.join(ICONS_DIR, file);
        const name = path.basename(file, '.svg');
        const svg = fs.readFileSync(filepath, 'utf8');
        sprites.add(name, svg);
    });

// 生成sprite文件
fs.writeFileSync(SPRITE_PATH, sprites.toString());

console.log('SVG sprite 已生成！'); 