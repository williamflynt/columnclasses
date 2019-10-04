from django.db import models

from columnclasses.models import TimeStampedModel


class Source(TimeStampedModel):
    """The CSV linking model from the file to Columns"""

    # The actual file
    document = models.FileField(upload_to="uploads")

    # time that we classified the Columns for this Source
    time_classified = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return self.document.name


class Classification(TimeStampedModel):
    """A type that a Column can be"""

    # what we are labeling the column - a target for a classifier
    label = models.CharField(max_length=255)

    # human words on what this is
    description = models.TextField(blank=True)

    # A Classification can be either a main classification or a sub-classification.
    main = models.BooleanField(default=False)

    # Main classifications will add sub-Classifications here.
    subclasses = models.ManyToManyField("self", blank=True)

    class Meta:
        ordering = ("id",)

    def __str__(self) -> str:
        return self.label


class Column(TimeStampedModel):
    """a column in a CSV"""

    # The CSV-storing model
    source = models.ForeignKey("Source", on_delete=models.CASCADE)

    # position of the column, left to right
    index = models.IntegerField()

    # The top level classification (address, name, etc)
    main_class = models.ForeignKey(
        "Classification", on_delete=models.SET_NULL, null=True
    )

    # The sub classification (mailing, property, full, first, etc)
    sub_class = models.ForeignKey(
        "Classification",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="columns",
    )

    # Descriptive stats as a JSON object (sqlite doesn't have JSONField)
    # analysis = JSONField(blank=True)
    analysis = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.source.document.name[:10]} - Column {self.index}"
