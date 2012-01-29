from django.contrib import admin

from representatives.models import Representative, RepresentativeSet

class RepresentativeSetAdmin(admin.ModelAdmin):

    actions = ['update_from_scraperwiki']

    def update_from_scraperwiki(self, request, queryset):
        for rset in queryset:
            num_updated = rset.update_from_scraperwiki()
            msg = "Updated %s representatives for %s." % (num_updated, rset)
            no_boundaries = Representative.objects.filter(representative_set=rset, boundary='').count()
            if no_boundaries:
                msg += " %s did not match a boundary." % no_boundaries
            else:
                msg += " All matched a boundary."
            self.message_user(request, msg)
    update_from_scraperwiki.short_description = "Update from ScraperWiki"
    
class RepresentativeAdmin(admin.ModelAdmin):
    list_display = ['name', 'representative_set', 'district_name', 'elected_office', 'boundary']
    list_filter = ['representative_set']
    search_fields = ['name', 'district_name', 'elected_office']
    
admin.site.register(Representative, RepresentativeAdmin)
admin.site.register(RepresentativeSet, RepresentativeSetAdmin)