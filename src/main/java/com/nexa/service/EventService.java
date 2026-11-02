package com.nexa.service;

import com.nexa.dto.EventRequest;
import com.nexa.dto.EventResponse;
import com.nexa.entity.Event;
import com.nexa.repository.EventRepository;
import org.springframework.stereotype.Service;
import com.nexa.exception.EventNotFoundException;

import java.util.List;

@Service
public class EventService {

    private final EventRepository eventRepository;

    public EventService(EventRepository eventRepository) {
        this.eventRepository = eventRepository;
    }

    public EventResponse createEvent(EventRequest request) {

        validateEventTime(request);

        Event event = new Event(
                request.getName(),
                request.getLocation(),
                request.getStartTime(),
                request.getEndTime(),
                request.getStatus()
        );

        Event savedEvent = eventRepository.save(event);

        return convertToResponse(savedEvent);
    }

    public List<EventResponse> getAllEvents() {

        return eventRepository.findAll()
                .stream()
                .map(this::convertToResponse)
                .toList();
    }

    public EventResponse getEventById(Long id) {

        Event event = eventRepository.findById(id)
                .orElseThrow(() ->
                        new EventNotFoundException("Event not found with id: " + id));

        return convertToResponse(event);
    }

    public EventResponse updateEvent(Long id, EventRequest request) {

        validateEventTime(request);

        Event event = eventRepository.findById(id)
                .orElseThrow(() ->
                        new EventNotFoundException("Event not found with id: " + id));

        event.setName(request.getName());
        event.setLocation(request.getLocation());
        event.setStartTime(request.getStartTime());
        event.setEndTime(request.getEndTime());
        event.setStatus(request.getStatus());

        Event updatedEvent = eventRepository.save(event);

        return convertToResponse(updatedEvent);
    }

    public void deleteEvent(Long id) {

        if (!eventRepository.existsById(id)) {
                throw new EventNotFoundException("Event not found with id: " + id);
            }

        eventRepository.deleteById(id);
    }

    private void validateEventTime(EventRequest request) {

        if (!request.getEndTime().isAfter(request.getStartTime())) {
            throw new IllegalArgumentException(
                    "End time must be after start time");
        }
    }

    private EventResponse convertToResponse(Event event) {

        return new EventResponse(
                event.getId(),
                event.getName(),
                event.getLocation(),
                event.getStartTime(),
                event.getEndTime(),
                event.getStatus()
        );
    }
}