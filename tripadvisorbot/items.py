from scrapy.item import Item, Field

# Default item
class Website(Item):

	name = Field()
	description = Field()
	url = Field()


# TripAdvisor items
class GlobalItem(Item):
	location = Field()
	cat = Field()
	details = Field()

class TripAdvisorItem(Item):

	name = Field()
	address = Field()
	url = Field()
	# avg_stars = Field()
	# photos = Field()
	# reviews = Field()

class TripAdvisorAddressItem(Item):

	street = Field()
	postal_code = Field()
	locality = Field()
	# country = Field()
	phone = Field()
	email = Field()
	website = Field()

class TripAdvisorPhotoItem(Item):
	# URL to image.
	url = Field()
	
class TripAdvisorReviewItem(Item):

	date = Field()
	title = Field()
	description = Field()
	stars = Field()
	helpful_votes = Field()

	user = Field()

class TripAdvisorUserItem(Item):

	url = Field()
	name = Field()
	address = Field()