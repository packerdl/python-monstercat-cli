from marshmallow import EXCLUDE, Schema, fields


class MonstercatSchema(Schema):
    class Meta:
        unknown = EXCLUDE


class Release(MonstercatSchema):
    id = fields.Str(data_key="Id")
    artists_title = fields.Str(data_key="ArtistsTitle")
    brand = fields.Str(data_key="Brand")
    catalog_id = fields.Str(data_key="CatalogId")
    downloadable = fields.Bool(data_key="Downloadable")
    genre_primary = fields.Str(data_key="GenrePrimary")
    genre_secondary = fields.Str(data_key="GenreSecondary")
    in_early_access = fields.Bool(data_key="InEarlyAccess")
    release_data = fields.DateTime(data_key="ReleaseDate")
    release_type = fields.Str(data_key="type")
    streamable = fields.Bool(data_key="Streamable")
    title = fields.Str(data_key="Title")


class Track(MonstercatSchema):
    id = fields.Str(data_key="Id")
    artists_title = fields.Str(data_key="ArtistsTitle")
    bpm = fields.Int(data_key="BPM")
    brand = fields.Str(data_key="Brand")
    debut_date = fields.DateTime(data_key="DebutDate")
    downloadable = fields.Bool(data_key="Downloadable")
    duration = fields.Int(data_key="Duration")
    explicit = fields.Bool(data_key="Explicit")
    genre_primary = fields.Str(data_key="GenrePrimary")
    genre_secondary = fields.Str(data_key="GenreSecondary")
    in_early_access = fields.Bool(data_key="InEarlyAccess")
    streamable = fields.Bool(data_key="Streamable")
    title = fields.Str(data_key="Title")
    track_number = fields.Int(data_key="TrackNumber")


class UserSettings(MonstercatSchema):
    playlist_public_default = fields.Bool(data_key="PlaylistPublicDefault")
    preferred_format = fields.Str(data_key="PreferredFormat")


class User(MonstercatSchema):
    id = fields.Str(data_key="Id")
    created_at = fields.DateTime(data_key="CreatedAt")
    updated_at = fields.DateTime(data_key="UpdatedAt")
    has_gold = fields.Bool(data_key="HasGold")
    settings = fields.Nested(UserSettings, data_key="Settings")
