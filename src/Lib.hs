{-# LANGUAGE Strict #-}

module Lib
    ( someFunc
    ) where

import Data.Vector (Vector)
import Data.Word (Word64)

someFunc :: IO ()
someFunc = putStrLn "someFunc"

type Fp = Float
data NDC = NDC Fp Fp
data UV = UV Fp Fp
data P3 = P3 Fp Fp Fp
data V3 = V3 Fp Fp Fp
data N3 = N3 Fp Fp Fp
data Color = Color Fp Fp Fp
data Ray = Ray
  { orgn :: P3
  , dirn :: V3
  }
data Shader = Shader
  { sample :: P3 -> N3 -> Vector Ray
  , shade :: Vector Ray -> Color
  }
data TraceResult = NoHit
                 | Hit P3 N3
newtype Traceable = Traceable (Vector Ray -> Vector TraceResult)
data Geom = Geom Traceable Shader

sphere :: P3 -> Fp -> Traceable
sphere = undefined

tri :: P3 -> P3 -> P3 -> Traceable
tri = undefined

quad :: P3 -> P3 -> P3 -> P3 -> Traceable
quad = undefined

lambert :: Color -> Shader
lambert = undefined

emission :: Color -> Shader
emission = undefined

----------------------------------

type RayContext = Word64

data Sample = Sample NDC RayContext

data Shade = Shade Shader RayContext

data DeferredRay = DeferredRay
  { context :: RayContext
  , ray :: Ray
  }

data TraceLayer a = TraceLayer
  { instructions :: Vector a
  , rays :: Vector DeferredRay
  }

type PrimaryRays = TraceLayer Sample
type SecondaryRays = TraceLayer Shade
