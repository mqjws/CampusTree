import type {
  CampusNotice,
  CommentRecord,
  PostRecord,
  ProfileRecord,
  TopicItem,
} from '@/types/content'

export const mockPosts: PostRecord[] = [
  {
    id: 1,
    title: '图书馆三楼靠窗的位置下午四点后最安静',
    summary: '最近几周踩点之后发现，三楼靠窗那一排在下午四点后空位率明显更高，适合赶作业和复习。',
    content:
      '最近几周踩点之后发现，图书馆三楼靠窗那一排在下午四点后空位率明显更高，适合赶作业和复习。\n\n如果你是喜欢安静但又不想太偏的类型，这个区域比自习室更轻松，也不容易被打断。\n\n唯一的问题是插座不算多，建议先把电脑充一部分电再去。',
    category: '学习',
    relativeTime: '5 分钟前',
    fullTime: '2026-06-18 19:45',
    likeCount: 128,
    commentCount: 18,
    author: {
      id: 101,
      alias: '匿名同学 A',
      avatarEmoji: '🌿',
    },
  },
  {
    id: 2,
    title: '食堂新开的麻辣香锅窗口比预想中稳很多',
    summary: '本来以为会踩雷，结果味道、出餐速度和性价比都还不错，中午排队也没有特别夸张。',
    content:
      '本来以为食堂新开的麻辣香锅窗口会踩雷，结果味道、出餐速度和性价比都还不错。\n\n中午排队也没有特别夸张，荤素搭配的自由度比较高，比较适合课间时间紧但又想吃热一点的同学。',
    category: '美食',
    relativeTime: '22 分钟前',
    fullTime: '2026-06-18 19:28',
    likeCount: 94,
    commentCount: 11,
    author: {
      id: 102,
      alias: '匿名同学 B',
      avatarEmoji: '🍜',
    },
  },
  {
    id: 3,
    title: '这周社团招新的摊位布置比往年认真很多',
    summary: '路过操场一圈，明显感觉今年大家更重视视觉呈现了，信息牌和互动区都更完整。',
    content:
      '今天路过操场一圈，感觉今年社团招新的摊位布置比往年认真很多。\n\n很多社团都做了完整的信息牌和互动区，哪怕只是去逛一圈也能看出来活动准备度挺高。',
    category: '校园',
    relativeTime: '1 小时前',
    fullTime: '2026-06-18 18:40',
    likeCount: 72,
    commentCount: 9,
    author: {
      id: 103,
      alias: '匿名同学 C',
      avatarEmoji: '🎪',
    },
  },
]

export const mockCommentsByPostId: Record<number, CommentRecord[]> = {
  1: [
    {
      id: 201,
      content: '感谢分享，明天就去试试这个位置。',
      relativeTime: '3 分钟前',
      likeCount: 8,
      author: {
        id: 301,
        alias: '匿名同学 D',
        avatarEmoji: '📚',
      },
    },
    {
      id: 202,
      content: '靠窗的位置光线确实好，就是插座比较少。',
      relativeTime: '14 分钟前',
      likeCount: 5,
      author: {
        id: 302,
        alias: '匿名同学 E',
        avatarEmoji: '☕',
      },
    },
    {
      id: 203,
      content: '周末去会不会人更多？',
      relativeTime: '27 分钟前',
      likeCount: 2,
      author: {
        id: 303,
        alias: '匿名同学 F',
        avatarEmoji: '🪟',
      },
    },
  ],
  2: [
    {
      id: 204,
      content: '我昨天也吃了，辣度比想象中稳定。',
      relativeTime: '12 分钟前',
      likeCount: 4,
      author: {
        id: 304,
        alias: '匿名同学 G',
        avatarEmoji: '🌶️',
      },
    },
  ],
  3: [
    {
      id: 205,
      content: '今年路过真的会忍不住多停几分钟。',
      relativeTime: '18 分钟前',
      likeCount: 3,
      author: {
        id: 305,
        alias: '匿名同学 H',
        avatarEmoji: '🎈',
      },
    },
  ],
}

export const mockTopics: TopicItem[] = [
  { id: 1, label: '期末复习', postCount: 32 },
  { id: 2, label: '食堂测评', postCount: 24 },
  { id: 3, label: '社团招新', postCount: 18 },
  { id: 4, label: '宿舍吐槽', postCount: 12 },
]

export const mockNotices: CampusNotice[] = [
  {
    id: 1,
    title: '本周产品演示',
    content: '当前页面全部使用占位数据，结构和交互节奏优先于真实业务接入。',
  },
  {
    id: 2,
    title: '下一阶段计划',
    content: '后续将接入帖子列表、帖子详情、评论列表和用户中心相关 API。',
  },
]

export const mockProfile: ProfileRecord = {
  userId: '#1024',
  nickname: '匿名同学',
  joinedAt: '2026-06-17',
  tagline: '先把真实想法说出来，再慢慢决定要不要解释。',
  stats: {
    posts: 12,
    comments: 45,
    likes: 86,
  },
}

export const createPostCategories = ['学习', '美食', '校园', '吐槽', '生活']

export function getPostById(id: number): PostRecord | undefined {
  return mockPosts.find((post) => post.id === id)
}

export function getCommentsByPostId(id: number): CommentRecord[] {
  return mockCommentsByPostId[id] || []
}
