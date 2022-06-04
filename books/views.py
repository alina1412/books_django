
from django.http import HttpResponseRedirect
from django.urls import reverse

import logging
logger = logging.getLogger(__name__)


def home_redirect(request):
    logger.info("home_view")
    return HttpResponseRedirect(reverse('users:home'))
