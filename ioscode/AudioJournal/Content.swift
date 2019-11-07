//
//  Message.swift
//  AudioJournal
//
//  Created by Shruti Jana on 10/26/19.
//  Copyright © 2019 Shruti Jana. All rights reserved.
//

import Foundation

final class Content: Codable {
    var id: Int?
    var message: String
    
    init(message: String) {
        self.message = message
    }
}
 
