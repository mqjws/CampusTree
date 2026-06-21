export interface AuthorSummary {
  id: number
  alias: string
  avatarEmoji: string
}

export interface PostRecord {
  id: number
  title: string
  summary: string
  content: string
  category: string
  relativeTime: string
  fullTime: string
  viewCount: number
  likeCount: number
  commentCount: number
  likedByCurrentUser: boolean
  allowComments: boolean
  topicId: number | null
  topicName: string | null
  author: AuthorSummary
}

export interface CommentRecord {
  id: number
  content: string
  relativeTime: string
  fullTime: string
  postId: number
  postTitle: string
  likeCount: number
  author: AuthorSummary
}

export interface TopicItem {
  id: number
  label: string
  postCount: number
}

export interface CampusNotice {
  id: number
  title: string
  content: string
}

export interface ProfileStats {
  posts: number
  comments: number
  likes: number
  views: number
  latestPostAt: string | null
  latestCommentAt: string | null
}

export interface ProfileRecord {
  userId: string
  nickname: string
  joinedAt: string
  tagline: string
  stats: ProfileStats
}
