//
//  RecordViewModel.swift
//  AudioJournal
//
//  Created by Shruti Jana on 10/26/19.
//  Copyright © 2019 Shruti Jana. All rights reserved.
//

import Foundation
import UIKit

class RecordView: UICollectionViewCell {
    
    @IBOutlet var label: UILabel!
    
    required init?(coder aDecoder: NSCoder) {
        super.init(coder: aDecoder)
        let view = UIView(frame: self.frame)
        view.autoresizingMask = [.flexibleWidth, .flexibleHeight]
        view.backgroundColor = UIColor(red: 0.2, green: 0.6, blue: 1.0, alpha: 1.0)
        view.layer.borderColor = UIColor.white.cgColor
        view.layer.borderWidth = 4
        self.selectedBackgroundView = view
    }

}
