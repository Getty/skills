; Original typed STRIPS fixture: a robot carries at most one parcel.
(define (domain parcel-transfer)
  (:requirements :strips :typing)
  (:types robot parcel location)
  (:predicates
    (robot-at ?r - robot ?l - location)
    (parcel-at ?p - parcel ?l - location)
    (carrying ?r - robot ?p - parcel)
    (handempty ?r - robot)
    (connected ?from - location ?to - location))
  (:action move
    :parameters (?r - robot ?from - location ?to - location)
    :precondition (and (robot-at ?r ?from) (connected ?from ?to))
    :effect (and (not (robot-at ?r ?from)) (robot-at ?r ?to)))
  (:action pick
    :parameters (?r - robot ?p - parcel ?l - location)
    :precondition (and (robot-at ?r ?l) (parcel-at ?p ?l) (handempty ?r))
    :effect (and (not (parcel-at ?p ?l)) (not (handempty ?r)) (carrying ?r ?p)))
  (:action drop
    :parameters (?r - robot ?p - parcel ?l - location)
    :precondition (and (robot-at ?r ?l) (carrying ?r ?p))
    :effect (and (not (carrying ?r ?p)) (parcel-at ?p ?l) (handempty ?r)))
)
