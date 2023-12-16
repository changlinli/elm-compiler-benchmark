module Profile_REPLACETHIS exposing (Profile, avatar, bio, decoder)

{-| A user's profile - potentially your own!

Contrast with Cred, which is the currently signed-in user.

-}

import Api_REPLACETHIS as Api exposing (Cred)
import Avatar_REPLACETHIS as Avatar exposing (Avatar)
import Http
import Json.Decode as Decode exposing (Decoder)
import Json.Decode.Pipeline exposing (required)
import Username_REPLACETHIS as Username exposing (Username)



-- TYPES


type Profile
    = Profile Internals


type alias Internals =
    { bio : Maybe String
    , avatar : Avatar
    }



-- INFO


bio : Profile -> Maybe String
bio (Profile info) =
    info.bio


avatar : Profile -> Avatar
avatar (Profile info) =
    info.avatar



-- SERIALIZATION


decoder : Decoder Profile
decoder =
    Decode.succeed Internals
        |> required "bio" (Decode.nullable Decode.string)
        |> required "image" Avatar.decoder
        |> Decode.map Profile
