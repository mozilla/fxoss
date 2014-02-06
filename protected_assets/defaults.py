from mezzanine.conf import register_setting


register_setting(
    name="DOWNLOAD_AGREEMENT_VERSION",
    description="Current version of the download agreement.",
    editable=True,
    default='1.0',
)