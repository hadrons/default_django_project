from django.views.generic import TemplateView


class HomeSiteView(TemplateView):
	template_name = 'homesite/home.html'
