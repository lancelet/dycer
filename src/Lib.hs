module Lib
    ( someFunc
    ) where

import Data.Vector (Vector)

someFunc :: IO ()
someFunc = putStrLn "someFunc"

{-
type FPType = Float

newtype Pt3 = Pt3 (V3 FPType)

newtype Vec3 = Vec3 (V3 FPType)

newtype Nor3 = Nor3 (V3 FPType)

newtype Color = Color (V3 FPType)

data Ray = Ray
  { rayO :: !Pt3
  , rayD :: !Vec3
  }

data Shader = Shader
  { shaderSample :: Pt3 -> Nor3 -> Vector Ray
  , shaderShade :: Vector Ray -> Color
  }

data TraceResult = NoHit
                 | TraceHit Pt3 Vec3

newtype Traceable = Traceable (Ray -> TraceResult)

data Geom = Geom Traceable Shader

sphere :: Pt3 -> Double -> Traceable
sphere = undefined

tri :: Pt3 -> Pt3 -> Pt3 -> Traceable
tri = undefined

quad :: Pt3 -> Pt3 -> Pt3 -> Pt3 -> Traceable
quad = undefined

lambert :: Color -> Shader
lambert = undefined

emission :: Color -> Shader
emission = undefined

----------------------------------

type ContextId = Long

data Deferred a = Deferred
  { defContext :: ContextId
  , defValue :: a
  }

type DeferredRay = Deferred Ray

type DeferredColor = Deferred Color

data ShaderContext = ShaderContext
  { scContextId :: ContextId
  , scShader :: Shader
  }

-}
