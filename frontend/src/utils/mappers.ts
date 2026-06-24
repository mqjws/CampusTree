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
        views: 0,
        latestPostAt: null,
        latestCommentAt: null,
      },
    }
  }

  return {
    userId: `#${user.id}`,
    nickname: user.nickname,
    joinedAt: formatFullTime(user.created_at),
    tagline: '当前用户数据与统计信息均来自真实接口。',
    stats: stats || {
      posts: 0,
      comments: 0,
      likes: 0,
      views: 0,
      latestPostAt: null,
      latestCommentAt: null,
    },
  }
}

export function mapPostDtoToRecord(post: PostDto): PostRecord {
  const summary = post.content.trim()
    ? post.content.length > 120
      ? `${post.content.slice(0, 120)}...`
      : post.content
    : '暂无正文'

  return {
    id: post.id,
    title: post.title,
    summary,
    content: post.content,
    category: post.category,
    relativeTime: formatRelativeTime(post.created_at),
    fullTime: formatFullTime(post.created_at),
    viewCount: post.view_count,
    likeCount: post.like_count,
    commentCount: post.comment_count,
    likedByCurrentUser: post.liked_by_current_user,
    allowComments: post.allow_comments,
    registeredOnly: post.registered_only,
    topicId: post.topic_id,
    topicName: post.topic_name,
    author: {
      id: post.author_id,
      alias: post.author_nickname,
      avatarEmoji: pickEmoji(post.author_id),
    },
  }
}

export function mapCommentDtoToRecord(comment: CommentDto): CommentRecord {
  return {
    id: comment.id,
    content: comment.content,
    relativeTime: formatRelativeTime(comment.created_at),
    fullTime: formatFullTime(comment.created_at),
    postId: comment.post_id,
    postTitle: comment.post_title || `帖子 #${comment.post_id}`,
    likeCount: 0,
    author: {
      id: comment.author_id,
      alias: comment.author_nickname || `用户 #${comment.author_id}`,
      avatarEmoji: pickEmoji(comment.author_id),
    },
  }
}
