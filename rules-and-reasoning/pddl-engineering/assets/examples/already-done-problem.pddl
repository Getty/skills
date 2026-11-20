; The goal is initially satisfied; an empty plan is valid.
(define (problem already-delivered)
  (:domain parcel-transfer)
  (:objects bot - robot parcel-a - parcel dock lab - location)
  (:init (robot-at bot lab) (parcel-at parcel-a lab) (handempty bot))
  (:goal (and (parcel-at parcel-a lab) (handempty bot)))
)
