
set(relopec_sv_subscriber_SRCS
   relopec_sv_subscriber.c
)

IF(MSVC)

set_source_files_properties(${relopec_sv_subscriber_SRCS}
                                       PROPERTIES LANGUAGE CXX)
ENDIF(MSVC)
                                       
add_executable(relopec_sv_subscriber
  ${relopec_sv_subscriber_SRCS}
)

target_link_libraries(relopec_sv_subscriber
    iec61850
)
