import type { CommentRecord, PostRecord, ProfileRecord, ProfileStats } from '@/types/content'
import type { CommentDto, PostDto, UserDto } from '@/types/api'
import { formatFullTime, formatRelativeTime } from './format'

const fallbackEmojis = ['🌿', '📚', '☕', '🎈', '🫧', '🍜', '🎪', '🌙']

function pickEmoji(id: number): string {
  return fallbackEmojis[id % fallbackEmojis.length]
}

export function mapUserToProfile(user: UserDto | null, stats?: ProfileStats): ProfileRecord {
  if (!user) {
    return {
      userId: '#----',
      nickname: '匿名同学',
      joinedAt: '--',
      tagline: '登录后查看你的账户信息与内容记录。',
      stats: stats || {
        posts: 0,
        comments: 0,
        likes: 0,
      },
    }
  }

  return {
    userId: `#${user.id}`,
    nickname: user.username,
    joinedAt: formatFullTime(user.created_at),
    tagline: '当前用户数据与统计信息均来自真实接口。',
    stats: stats || {
      posts: 0,
      comments: 0,
      likes: 0,
    },
  }
}

export function mapPostDtoToRecord(post: PostDto): PostRecord {
  return {
    id: post.id,
    title: post.title,
    summary: post.content.length > 120 ? `${post.content.slice(0, 120)}...` : post.content,
    content: post.content,
    category: '未分类',
    relativeTime: formatRelativeTime(post.created_at),
    fullTime: formatFullTime(post.created_at),
    likeCount: 0,
    commentCount: post.comment_count,
    author: {
      id: post.author_id,
      alias: `用户 #${post.author_id}`,
      avatarEmoji: pickEmoji(post.author_id),
    },
  }
}

export function mapCommentDtoToRecord(comment: CommentDto): CommentRecord {
  return {
    id: comment.id,
    content: comment.content,
    relativeTime: formatRelativeTime(comment.created_at),
    likeCount: 0,
    author: {
      id: comment.author_id,
      alias: `用户 #${comment.author_id}`,
      avatarEmoji: pickEmoji(comment.author_id),
    },
  }
}
