{-# LANGUAGE TemplateHaskell #-}

module Dycer.Blender.Types where

import Data.Aeson (ToJSON, FromJSON)
import Data.Aeson.TH (deriveJSON, defaultOptions, fieldLabelModifier)
import Data.Char (toLower)

data Vec3 = Vec3
    { v3x :: Float
    , v3y :: Float
    , v3z :: Float
    } deriving (Show, Eq)

$(deriveJSON defaultOptions { fieldLabelModifier = drop 2 } ''Vec3)

vec3Sample :: Vec3
vec3Sample = Vec3 1.0 2.0 3.0


data AxisAngle = AxisAngle
    { aaAngle :: Float
    , aaAxis  :: Vec3
    } deriving (Show, Eq)

$(deriveJSON
  defaultOptions { fieldLabelModifier = map toLower . drop 2 }
  ''AxisAngle)

aaSample :: AxisAngle
aaSample = AxisAngle 45.0 vec3Sample


data Camera = Camera
    { camFov :: Float
    , camRotation :: AxisAngle
    , camTranslation :: Vec3
    } deriving (Show, Eq)

$(deriveJSON
  defaultOptions { fieldLabelModifier = map toLower . drop 3 }
  ''Camera)

camSample :: Camera
camSample = Camera 50.0 aaSample vec3Sample


data Scene = Scene
    { scCamera :: Camera
    , scXres :: Int
    , scYres :: Int
    } deriving (Show, Eq)

$(deriveJSON
 defaultOptions { fieldLabelModifier = map toLower . drop 2 }
 ''Scene
 )

sceneSample :: Scene
sceneSample = Scene camSample 960 540
