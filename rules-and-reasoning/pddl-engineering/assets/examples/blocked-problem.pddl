; No route reaches the lab; the finite STRIPS task is unsolvable.
(define (problem blocked-delivery)
  (:domain parcel-transfer)
  (:objects bot - robot parcel-a - parcel dock lab - location)
  (:init (robot-at bot dock) (parcel-at parcel-a dock) (handempty bot))
  (:goal (and (parcel-at parcel-a lab) (handempty bot)))
)
