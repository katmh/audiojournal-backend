//
//  apiRequests.swift
//  AudioJournal
//
//  Created by Shruti Jana on 10/26/19.
//  Copyright © 2019 Shruti Jana. All rights reserved.
//

import Foundation

enum APIError: Error {
    case responseProblem
    case decodingProblem
    case encodingProblem
}

extension Dictionary {
    func percentEscaped() -> String {
        return map { (key, value) in
            let escapedKey = "\(key)".addingPercentEncoding(withAllowedCharacters: .urlQueryValueAllowed) ?? ""
            let escapedValue = "\(value)".addingPercentEncoding(withAllowedCharacters: .urlQueryValueAllowed) ?? ""
            return escapedKey + "=" + escapedValue
        }
        .joined(separator: "&")
    }
}

extension CharacterSet {
    static let urlQueryValueAllowed: CharacterSet = {
        let generalDelimitersToEncode = ":#[]@" // does not include "?" or "/" due to RFC 3986 - Section 3.4
        let subDelimitersToEncode = "!$&'()*+,;="

        var allowed = CharacterSet.urlQueryAllowed
        allowed.remove(charactersIn: "\(generalDelimitersToEncode)\(subDelimitersToEncode)")
        return allowed
    }()
}

struct APIRequest {
    let resourceURL: URL
    init(endpoint: String) {
        let resourceString = "http://localhost:8080/api/\(endpoint)"
        guard let resourceURL = URL(string:resourceString) else { fatalError() }
        self.resourceURL = resourceURL
    }
    
    func save (_ messageToSave: Content, completion: @escaping(Result<Content, APIError>) -> Void) {
        do {
            let url = URL(string: "https://4f1d66fb.ngrok.io")!
            var request = URLRequest(url: url)
            request.setValue("application/x-www-form-urlencoded", forHTTPHeaderField: "Content-Type")
            request.httpMethod = "POST"
            let parameters: [String: Any] = [
                "id": 13,
                "name": messageToSave.message,
                "location": "",
                "transcript": "Hello, how are you doing today. I'm okay doctor Phins, but my eye has been pretty swollen for the past few days. My pupil has been dialated and I have multiple red streaks. I don't think this is necessarily an allergy because I've never been diagnosed with any. Hmm okay let me take a look at it more closely. I think it could possibly be Blepharitis or pink eye. Have you had any fever recently or been around others who have? Nope."
            ]
            request.httpBody = parameters.percentEscaped().data(using: .utf8)

            let task = URLSession.shared.dataTask(with: request) { data, response, error in
                guard let data = data,
                    let response = response as? HTTPURLResponse,
                    error == nil else {                                              // check for fundamental networking error
                    print("error", error ?? "Unknown error")
                    return
                }

                guard (200 ... 299) ~= response.statusCode else {                    // check for http errors
                    print("statusCode should be 2xx, but is \(response.statusCode)")
                    print("response = \(response)")
                    return
                }

                let responseString = String(data: data, encoding: .utf8)
                print("responseString = \(responseString)")
            }

        task.resume()
        } catch {
            completion(.failure(.encodingProblem))
        }
    }
}

