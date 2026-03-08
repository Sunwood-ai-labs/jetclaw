import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'JetClaw',
  description: 'Waveshare JetBot 2GB + PicoClaw on Jetson Nano 2GB',
  lang: 'en-US',
  base: '/jetclaw/',
  cleanUrls: true,
  lastUpdated: true,
  head: [['link', { rel: 'icon', href: '/images/favicon.png' }]],
  vite: {
    assetsInclude: ['**/*.JPG', '**/*.JPEG', '**/*.PNG', '**/*.GIF']
  },
  themeConfig: {
    logo: '/images/logo.png',
    siteTitle: 'JetClaw',
    nav: [
      { text: 'Guide', link: '/getting_started' },
      { text: 'Waveshare', link: '/jetclaw/waveshare-jetbot-2gb' },
      { text: 'PicoClaw', link: '/jetclaw/picoclaw' },
      { text: 'GitHub', link: 'https://github.com/Sunwood-ai-labs/jetclaw' }
    ],
    sidebar: [
      {
        text: 'JetClaw',
        items: [
          { text: 'Home', link: '/' },
          { text: 'Getting Started', link: '/getting_started' },
          { text: 'Waveshare JetBot 2GB', link: '/jetclaw/waveshare-jetbot-2gb' },
          { text: 'PicoClaw Integration', link: '/jetclaw/picoclaw' },
          { text: 'Operations', link: '/jetclaw/operations' }
        ]
      },
      {
        text: 'Examples',
        collapsed: false,
        items: [
          { text: 'Basic Motion', link: '/examples/basic_motion' },
          { text: 'Teleoperation', link: '/examples/teleoperation' },
          { text: 'Collision Avoidance', link: '/examples/collision_avoidance' },
          { text: 'Road Following', link: '/examples/road_following' },
          { text: 'Object Following', link: '/examples/object_following' },
          { text: 'Community Examples', link: '/examples/community_examples' }
        ]
      },
      {
        text: 'Hardware and Software',
        collapsed: true,
        items: [
          { text: 'Bill of Materials', link: '/bill_of_materials' },
          { text: 'Bill of Materials (Orin)', link: '/bill_of_materials_orin' },
          { text: 'Hardware Setup', link: '/hardware_setup' },
          { text: 'SD Card Setup', link: '/software_setup/sd_card' },
          { text: 'Docker Setup', link: '/software_setup/docker' },
          { text: 'Native Setup', link: '/software_setup/native_setup' },
          { text: 'Wi-Fi Setup', link: '/software_setup/wifi_setup' }
        ]
      },
      {
        text: 'Reference',
        collapsed: true,
        items: [
          { text: 'Third Party Kits', link: '/third_party_kits' },
          { text: '3D Printing', link: '/3d_printing' },
          { text: 'Docker Tips', link: '/reference/docker_tips' },
          { text: 'Contributing', link: '/CONTRIBUTING' },
          { text: 'Changelog', link: '/CHANGELOG' }
        ]
      }
    ],
    socialLinks: [
      { icon: 'github', link: 'https://github.com/Sunwood-ai-labs/jetclaw' }
    ],
    search: {
      provider: 'local'
    },
    editLink: {
      pattern: 'https://github.com/Sunwood-ai-labs/jetclaw/edit/main/docs/:path'
    },
    footer: {
      message: 'JetClaw documentation for Waveshare JetBot 2GB and PicoClaw.',
      copyright: 'MIT'
    }
  }
})
