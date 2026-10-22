/**
 * update-assets.js
 * Utility to refresh or re-download local SVG assets for your GitHub Profile README.
 * Automatically removes all third-party watermarks, branding, and ads.
 * Run: node update-assets.js
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

const assetsDir = path.join(__dirname, 'assets');
if (!fs.existsSync(assetsDir)) {
  fs.mkdirSync(assetsDir, { recursive: true });
}

const items = [
  {
    name: 'hero-light.svg',
    url: 'https://www.gitskins.com/api/section/hero?username=raghavv1206&theme=aurora&avatar=https%3A%2F%2Favatars.githubusercontent.com%2Fu%2F148678214%3Fv%3D4&label=Raghav%20Mishra&mode=light'
  },
  {
    name: 'hero-dark.svg',
    url: 'https://www.gitskins.com/api/section/hero?username=raghavv1206&theme=aurora&avatar=https%3A%2F%2Favatars.githubusercontent.com%2Fu%2F148678214%3Fv%3D4&label=Raghav%20Mishra&mode=dark'
  },
  {
    name: 'wordmark-light.svg',
    url: 'https://www.gitskins.com/api/section/wordmark?username=raghavv1206&theme=aurora&avatar=https%3A%2F%2Favatars.githubusercontent.com%2Fu%2F148678214%3Fv%3D4&label=Raghav%20Mishra&v=cinematic-hero-wordmark-1&mode=light'
  },
  {
    name: 'wordmark-dark.svg',
    url: 'https://www.gitskins.com/api/section/wordmark?username=raghavv1206&theme=aurora&avatar=https%3A%2F%2Favatars.githubusercontent.com%2Fu%2F148678214%3Fv%3D4&label=Raghav%20Mishra&v=cinematic-hero-wordmark-1&mode=dark'
  },
  {
    name: 'highlights-light.svg',
    url: 'https://www.gitskins.com/api/section/highlights?username=raghavv1206&theme=aurora&avatar=https%3A%2F%2Favatars.githubusercontent.com%2Fu%2F148678214%3Fv%3D4&items=Python%3A%3ACurrent%20focus%7CJavaScript%3A%3AIn%20the%20active%20build%20queue%7CCSS%3A%3AIn%20the%20active%20build%20queue&v=cinematic-highlights-2&mode=light'
  },
  {
    name: 'highlights-dark.svg',
    url: 'https://www.gitskins.com/api/section/highlights?username=raghavv1206&theme=aurora&avatar=https%3A%2F%2Favatars.githubusercontent.com%2Fu%2F148678214%3Fv%3D4&items=Python%3A%3ACurrent%20focus%7CJavaScript%3A%3AIn%20the%20active%20build%20queue%7CCSS%3A%3AIn%20the%20active%20build%20queue&v=cinematic-highlights-2&mode=dark'
  },
  {
    name: 'stack-light.svg',
    url: 'https://www.gitskins.com/api/section/stack?username=raghavv1206&theme=aurora&avatar=https%3A%2F%2Favatars.githubusercontent.com%2Fu%2F148678214%3Fv%3D4&v=cinematic-stack-2&mode=light'
  },
  {
    name: 'stack-dark.svg',
    url: 'https://www.gitskins.com/api/section/stack?username=raghavv1206&theme=aurora&avatar=https%3A%2F%2Favatars.githubusercontent.com%2Fu%2F148678214%3Fv%3D4&v=cinematic-stack-2&mode=dark'
  },
  {
    name: 'projects-light.svg',
    url: 'https://www.gitskins.com/api/section/projects?username=raghavv1206&theme=aurora&avatar=https%3A%2F%2Favatars.githubusercontent.com%2Fu%2F148678214%3Fv%3D4&repos=raghavv1206%2FAdvision%2Craghavv1206%2Fget-me-a-chai-version-2%2Craghavv1206%2FPROMPTPAL%2Craghavv1206%2FBittree&v=cinematic-projects-2&mode=light'
  },
  {
    name: 'projects-dark.svg',
    url: 'https://www.gitskins.com/api/section/projects?username=raghavv1206&theme=aurora&avatar=https%3A%2F%2Favatars.githubusercontent.com%2Fu%2F148678214%3Fv%3D4&repos=raghavv1206%2FAdvision%2Craghavv1206%2Fget-me-a-chai-version-2%2Craghavv1206%2FPROMPTPAL%2Craghavv1206%2FBittree&v=cinematic-projects-2&mode=dark'
  },
  {
    name: 'city-light.svg',
    url: 'https://www.gitskins.com/api/section/city?username=raghavv1206&theme=aurora&avatar=https%3A%2F%2Favatars.githubusercontent.com%2Fu%2F148678214%3Fv%3D4&mode=light'
  },
  {
    name: 'city-dark.svg',
    url: 'https://www.gitskins.com/api/section/city?username=raghavv1206&theme=aurora&avatar=https%3A%2F%2Favatars.githubusercontent.com%2Fu%2F148678214%3Fv%3D4&mode=dark'
  },
  {
    name: 'chess-light.svg',
    url: 'https://www.gitskins.com/api/section/chess?username=raghavv1206&theme=aurora&avatar=https%3A%2F%2Favatars.githubusercontent.com%2Fu%2F148678214%3Fv%3D4&v=cinematic-chess-1&mode=light'
  },
  {
    name: 'chess-dark.svg',
    url: 'https://www.gitskins.com/api/section/chess?username=raghavv1206&theme=aurora&avatar=https%3A%2F%2Favatars.githubusercontent.com%2Fu%2F148678214%3Fv%3D4&v=cinematic-chess-1&mode=dark'
  },
  {
    name: 'social-light.svg',
    url: 'https://www.gitskins.com/api/section/social?username=raghavv1206&theme=aurora&avatar=https%3A%2F%2Favatars.githubusercontent.com%2Fu%2F148678214%3Fv%3D4&v=cinematic-social-2&mode=light'
  },
  {
    name: 'social-dark.svg',
    url: 'https://www.gitskins.com/api/section/social?username=raghavv1206&theme=aurora&avatar=https%3A%2F%2Favatars.githubusercontent.com%2Fu%2F148678214%3Fv%3D4&v=cinematic-social-2&mode=dark'
  }
];

function cleanSvg(data) {
  return data
    .replace(/<text[^>]*>[^<]*gitskins\.com[^<]*<\/text>/gi, '')
    .replace(/GitSkins\s*/gi, '');
}

function download(item) {
  return new Promise((resolve, reject) => {
    https.get(item.url, { headers: { 'User-Agent': 'Mozilla/5.0' } }, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        https.get(res.headers.location, (redirectRes) => {
          let data = '';
          redirectRes.on('data', chunk => data += chunk);
          redirectRes.on('end', () => {
            data = cleanSvg(data);
            fs.writeFileSync(path.join(assetsDir, item.name), data, 'utf8');
            console.log(`✓ Updated ${item.name} (${data.length} bytes)`);
            resolve();
          });
        }).on('error', reject);
        return;
      }
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        data = cleanSvg(data);
        fs.writeFileSync(path.join(assetsDir, item.name), data, 'utf8');
        console.log(`✓ Updated ${item.name} (${data.length} bytes)`);
        resolve();
      });
    }).on('error', reject);
  });
}

async function run() {
  console.log('Refreshing SVG assets...');
  for (const item of items) {
    try {
      await download(item);
    } catch (e) {
      console.error(`✗ Error on ${item.name}:`, e.message);
    }
  }
  console.log('Done!');
}

run();
