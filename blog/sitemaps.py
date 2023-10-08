from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(sitemaps):
	changefreq = 'weekly'
	priority = 0.9


	def items(self):
		return Post.published.all()


	def lastmod(self, obj):
		return obj.updated