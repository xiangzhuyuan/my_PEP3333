
Contents

*   [Preface for Readers of PEP 333](#preface-for-readers-of-pep-333)
*   [Abstract](#abstract)
*   [Original Rationale and Goals (from PEP 333)](#original-rationale-and-goals-from-pep-333)
*   [Specification Overview](#specification-overview)

    *   [A Note On String Types](#a-note-on-string-types)
    *   [The Application/Framework Side](#the-application-framework-side)
    *   [The Server/Gateway Side](#the-server-gateway-side)
    *   [Middleware: Components that Play Both Sides](#middleware-components-that-play-both-sides)

*   [Specification Details](#specification-details)

        *   [<tt class="docutils literal">environ</tt> Variables](#environ-variables)

                *   [Input and Error Streams](#input-and-error-streams)

        *   [The <tt class="docutils literal">start_response()</tt> Callable](#the-start-response-callable)

                *   [Handling the <tt class="docutils literal"><span class="pre">Content-Length</span></tt> Header](#handling-the-content-length-header)

        *   [Buffering and Streaming](#buffering-and-streaming)

                *   [Middleware Handling of Block Boundaries](#middleware-handling-of-block-boundaries)
        *   [The <tt class="docutils literal">write()</tt> Callable](#the-write-callable)

        *   [Unicode Issues](#unicode-issues)
    *   [Error Handling](#error-handling)
    *   [HTTP 1.1 Expect/Continue](#http-1-1-expect-continue)
    *   [Other HTTP Features](#other-http-features)
    *   [Thread Support](#thread-support)

*   [Implementation/Application Notes](#implementation-application-notes)

        *   [Server Extension APIs](#server-extension-apis)
    *   [Application Configuration](#application-configuration)
    *   [URL Reconstruction](#url-reconstruction)
    *   [Supporting Older (&lt;2.2) Versions of Python](#supporting-older-2-2-versions-of-python)
    *   [Optional Platform-Specific File Handling](#optional-platform-specific-file-handling)

*   [Questions and Answers](#questions-and-answers)
*   [Proposed/Under Discussion](#proposed-under-discussion)
*   [Acknowledgements](#acknowledgements)
*   [References](#references)
*   [Copyright](#copyright)